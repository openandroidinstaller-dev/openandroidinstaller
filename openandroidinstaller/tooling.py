"""This module contains functions to deal with tools like adb, fastboot and heimdall."""

# This file is part of OpenAndroidInstaller.
# OpenAndroidInstaller is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# OpenAndroidInstaller is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with OpenAndroidInstaller.
# If not, see <https://www.gnu.org/licenses/>."""
# Author: Tobias Sterbak

import sys
from pathlib import Path
import subprocess
from subprocess import (
    Popen,
    PIPE,
    STDOUT,
    CalledProcessError,
    CompletedProcess,
    check_output,
)
from time import sleep
from typing import List, Optional

from loguru import logger

PLATFORM = sys.platform


def run_command(tool: str, command: List[str], bin_path: Path) -> CompletedProcess:
    """Run a command with a tool (adb, fastboot, heimdall)."""
    yield f"${' '.join([tool] + command )}"
    if tool not in ["adb", "fastboot", "heimdall"]:
        raise Exception(f"Unknown tool {tool}. Use adb, fastboot or heimdall.")
    if PLATFORM == "win32":
        full_command = [str(bin_path.joinpath(Path(f"{tool}"))) + ".exe"] + command
        # prevent Windows from opening terminal windows
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        full_command = [str(bin_path.joinpath(Path(f"{tool}")))] + command
        si = None
    logger.info(f"Run command: {full_command}")
    # run the command
    with Popen(
        full_command,
        stdout=PIPE,
        stderr=STDOUT,
        bufsize=1,
        universal_newlines=True,
        startupinfo=si,
    ) as p:
        for line in p.stdout:
            logger.info(line.strip())
            yield line

    yield p.returncode == 0


def adb_reboot(bin_path: Path) -> bool:
    """Run adb reboot on the device and return success."""
    logger.info("Rebooting device with adb.")
    for line in run_command("adb", ["reboot"], bin_path):
        yield line
    if (type(line) == bool) and line:
        logger.debug("Reboot failed.")
        yield False
    else:
        yield True


def adb_reboot_bootloader(bin_path: Path) -> bool:
    """Reboot the device into bootloader and return success."""
    logger.info("Rebooting device into bootloader with adb.")
    for line in run_command("adb", ["reboot", "bootloader"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Reboot into bootloader failed.")
        yield False
        return
    sleep(1)
    yield True


def adb_reboot_download(bin_path: Path) -> bool:
    """Reboot the device into download mode of samsung devices and return success."""
    logger.info("Rebooting device into download mode with adb.")
    for line in run_command("adb", ["reboot", "download"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Reboot into download mode failed.")
        yield False
    else:
        # check if in download mode with heimdall?
        yield True


def adb_sideload(bin_path: Path, target: str) -> bool:
    """Sideload the target to device and return success."""
    logger.info("Rebooting device into bootloader with adb.")
    for line in run_command("adb", ["sideload", target], bin_path):
        yield line
    if (type(line) == bool) and line:
        logger.info(f"Sideloading {target} failed.")
        yield False
    else:
        yield True


def adb_twrp_copy_partitions(bin_path: Path, config_path: Path):
    # some devices like one plus 6t or motorola moto g7 power need the partitions copied to prevent a hard brick
    logger.info("Sideload copy_partitions script with adb.")
    # activate sideload
    for line in run_command("adb", ["shell", "twrp", "sideload"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Activating sideload failed.")
        yield False
        return
    # now sideload the script
    sleep(5)
    logger.info("Sideload the copy_partitions script")
    for line in run_command(
        "adb",
        [
            "sideload",
            f"{config_path.parent.joinpath(Path('copy-partitions-20220613-signed.zip'))}",
        ],
        bin_path,
    ):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Sideloading copy-partitions-20220613-signed.zip failed.")
    sleep(10)
    # reboot into the bootloader again
    logger.info("Rebooting device into bootloader with adb.")
    for line in run_command("adb", ["reboot", "bootloader"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Reboot into bootloader failed.")
        yield False
        return
    sleep(7)
    # Copy partitions end #
    return True


def adb_twrp_wipe_and_install(bin_path: Path, target: str, config_path: Path, install_addons=True) -> bool:
    """Wipe and format data with twrp, then flash os image with adb.

    Only works for twrp recovery.
    """
    logger.info("Wipe and format data with twrp, then install os image.")
    sleep(7)
    # now perform a factory reset
    for line in run_command("adb", ["shell", "twrp", "format", "data"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Formatting data failed.")
        yield False
        return
    sleep(1)
    # wipe some partitions
    for partition in ["cache", "system"]:
        for line in run_command("adb", ["shell", "twrp", "wipe", partition], bin_path):
            yield not line
        sleep(1)
        if (type(line) == bool) and not line:
            logger.error(f"Wiping {partition} failed.")
            yield False
            return
    # activate sideload
    logger.info("Wiping is done, now activate sideload.")
    for line in run_command("adb", ["shell", "twrp", "sideload"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Activating sideload failed.")
        yield False
        return
    # now flash os image
    sleep(5)
    logger.info("Sideload and install os image.")
    for line in run_command("adb", ["sideload", f"{target}"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error(f"Sideloading {target} failed.")
        # TODO: this might sometimes think it failed, but actually it's fine. So skip for now.
        # yield False
        # return
    # wipe some cache partitions
    sleep(7)
    for partition in ["dalvik", "cache"]:
        for line in run_command("adb", ["shell", "twrp", "wipe", partition], bin_path):
            yield line
        sleep(1)
        if (type(line) == bool) and not line:
            logger.error(f"Wiping {partition} failed.")
            # TODO: if this fails, a fix can be to just sideload something and then adb reboot
            for line in run_command(
                "adb",
                ["sideload", f"{config_path.parent.joinpath(Path('helper.txt'))}"],
                bin_path,
            ):
                yield line
            sleep(1)
            if (type(line) == bool) and not line:
                yield False
                return
            break
    # finally reboot into os
    sleep(7)
    if install_addons:
        # TODO: Fix the process for samsung devices
        # reboot into the bootloader again
        logger.info("Rebooting device into bootloader with adb.")
        for line in run_command("adb", ["reboot", "bootloader"], bin_path):
            yield line
        if (type(line) == bool) and not line:
            logger.error("Reboot into bootloader failed.")
            yield False
            return
        sleep(7)
    else:
        logger.info("Reboot into OS.")
        for line in run_command("adb", ["reboot"], bin_path):  # "shell", "twrp",
            yield line
        if (type(line) == bool) and not line:
            logger.error("Rebooting failed.")
            yield False
            return
        else:
            yield True


def fastboot_unlock_with_code(bin_path: Path, unlock_code: str) -> bool:
    """Unlock the device with fastboot and code given."""
    logger.info(f"Unlock the device with fastboot and code: {unlock_code}.")
    for line in run_command("fastboot", ["oem", "unlock", f"{unlock_code}"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error(f"Unlocking with code {unlock_code} failed.")
        yield False
    else:
        yield True


def fastboot_unlock(bin_path: Path) -> bool:
    """Unlock the device with fastboot and without code."""
    logger.info("Unlock the device with fastboot.")
    for line in run_command("fastboot", ["flashing", "unlock"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Unlocking failed.")
        yield False
    else:
        yield True


def fastboot_oem_unlock(bin_path: Path) -> bool:
    """OEM unlock the device with fastboot and without code."""
    logger.info("OEM unlocking the device with fastboot.")
    for line in run_command("fastboot", ["oem", "unlock"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("OEM unlocking failed.")
        yield False
    else:
        yield True


def fastboot_get_unlock_data(bin_path: Path) -> bool:
    """Get the unlock data with fastboot"""
    logger.info("Get unlock data with fastboot")
    for line in run_command("fastboot", ["oem", "get_unlock_data"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Getting unlock data failed.")
        yield False
    else:
        yield True


def fastboot_reboot(bin_path: Path) -> bool:
    """Reboot with fastboot"""
    logger.info("Rebooting device with fastboot.")
    for line in run_command("fastboot", ["reboot"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Rebooting with fastboot failed.")
        yield False
    else:
        yield True


def fastboot_flash_recovery(bin_path: Path, recovery: str) -> bool:
    """Temporarily, flash custom recovery with fastboot."""
    logger.info("Flash custom recovery with fastboot.")
    for line in run_command("fastboot", ["boot", f"{recovery}"], bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Flashing recovery failed.")
        yield False
    else:
        yield True


def heimdall_flash_recovery(bin_path: Path, recovery: str) -> bool:
    """Temporarily, flash custom recovery with heimdall."""
    logger.info("Flash custom recovery with heimdall.")
    for line in run_command(
        "heimdall", ["flash", "--no-reboot", "--RECOVERY", f"{recovery}"], bin_path
    ):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Flashing recovery with heimdall failed.")
        yield False
    else:
        yield True


def search_device(platform: str, bin_path: Path) -> Optional[str]:
    """Search for a connected device."""
    logger.info(f"Search devices on {platform} with {bin_path}...")
    try:
        # read device properties
        if platform in ("linux", "darwin"):
            output = check_output(
                [
                    str(bin_path.joinpath(Path("adb"))),
                    "shell",
                    "getprop",
                    "|",
                    "grep",
                    "ro.product.device",
                ],
                stderr=STDOUT,
            ).decode()
        elif platform in ("windows", "win32"):
            output = check_output(
                [
                    str(bin_path.joinpath(Path("adb.exe"))),
                    "shell",
                    "getprop",
                    "|",
                    "findstr",
                    "ro.product.device",
                ],
                stderr=STDOUT,
                shell=True,
            ).decode()
        else:
            raise Exception(f"Unknown platform {platform}.")
        device_code = output.split("[")[-1].strip()[:-1].strip()
        logger.info(device_code)
        return device_code
    except CalledProcessError:
        logger.error("Failed to detect a device.")
        return None
