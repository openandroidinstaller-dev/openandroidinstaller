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
    PIPE,
    STDOUT,
    CalledProcessError,
    check_output,
)
import shlex
from time import sleep
from typing import List, Optional, Union

from loguru import logger

PLATFORM = sys.platform


def run_command(
    command: str, bin_path: Path, enable_logging: bool = True
) -> Union[str, bool]:
    """Run a command with a tool (adb, fastboot, heimdall)."""
    yield f"${command}"
    # split the command and extract the tool part
    tool, *command = shlex.split(command)
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
    if enable_logging:
        logger.info(f"Run command: {full_command}")
    # run the command
    with subprocess.Popen(
        full_command,
        stdout=PIPE,
        stderr=STDOUT,
        bufsize=1,
        universal_newlines=True,
        startupinfo=si,
    ) as p:
        for line in p.stdout:
            if enable_logging:
                logger.info(line.strip())
            yield line.strip()

    # finally return if the command was successful
    yield p.returncode == 0


def add_logging(step_desc: str, return_if_fail: bool = False):
    """Logging decorator to wrap functions that yield lines.

    Logs the `step_desc`.
    """

    def logging_decorator(func):
        def logging(*args, **kwargs):
            logger.info(f"{step_desc} - Paramters: {kwargs}")
            for line in func(*args, **kwargs):
                if (type(line) == bool) and not line:
                    logger.error(f"{step_desc} Failed!")
                    if return_if_fail:
                        yield False
                        return
                yield line

        return logging

    return logging_decorator


@add_logging("Rebooting device with adb.")
def adb_reboot(bin_path: Path) -> bool:
    """Run adb reboot on the device and return success."""
    for line in run_command("adb reboot", bin_path):
        yield line


@add_logging("Rebooting device into bootloader with adb.", return_if_fail=True)
def adb_reboot_bootloader(bin_path: Path) -> Union[str, bool]:
    """Reboot the device into bootloader and return success."""
    for line in run_command("adb reboot bootloader", bin_path):
        yield line
    sleep(1)


@add_logging("Rebooting device into download mode with adb.")
def adb_reboot_download(bin_path: Path) -> Union[str, bool]:
    """Reboot the device into download mode of samsung devices and return success."""
    for line in run_command("adb reboot download", bin_path):
        yield line


@add_logging("Sideload the target to device with adb.")
def adb_sideload(bin_path: Path, target: str) -> Union[str, bool]:
    """Sideload the target to device and return success."""
    for line in run_command(f"adb sideload {target}", bin_path):
        yield line


@add_logging("Activate sideloading in TWRP.", return_if_fail=True)
def activate_sideload(bin_path: Path) -> Union[str, bool]:
    """Activate sideload with adb shell in twrp."""
    for line in run_command("adb shell twrp sideload", bin_path):
        yield line


def adb_twrp_copy_partitions(bin_path: Path, config_path: Path):
    # some devices like one plus 6t or motorola moto g7 power need the partitions copied to prevent a hard brick
    logger.info("Sideload copy_partitions script with adb.")
    # activate sideload
    for line in activate_sideload(bin_path):
        yield line
    # now sideload the script
    sleep(5)
    logger.info("Sideload the copy_partitions script")
    for line in adb_sideload(
        bin_path=bin_path,
        target=f"{config_path.parent.joinpath(Path('copy-partitions-20220613-signed.zip'))}",
    ):
        yield line
    sleep(10)
    # reboot into the bootloader again
    for line in adb_reboot_bootloader(bin_path):
        yield line
    sleep(7)
    # Copy partitions end #
    return True


@add_logging("Perform a factory reset with adb and twrp.", return_if_fail=True)
def adb_twrp_format_data(bin_path: Path):
    """Perform a factory reset with twrp and adb."""
    for line in run_command("adb shell twrp format data", bin_path):
        yield line


@add_logging("Wipe the selected partition with adb and twrp.", return_if_fail=True)
def adb_twrp_wipe_partition(bin_path: Path, partition: str):
    """Perform a factory reset with twrp and adb."""
    for line in run_command(f"adb shell twrp wipe {partition}", bin_path):
        yield line


def adb_twrp_wipe_and_install(
    bin_path: Path,
    target: str,
    config_path: Path,
    is_ab: bool,
    install_addons=True,
    recovery: str = None,
) -> bool:
    """Wipe and format data with twrp, then flash os image with adb.

    Only works for twrp recovery.
    """
    logger.info("Wipe and format data with twrp, then install os image.")
    sleep(7)
    # now perform a factory reset
    for line in adb_twrp_format_data(bin_path):
        yield line

    sleep(1)
    # wipe some partitions
    for partition in ["cache", "system"]:
        for line in adb_twrp_wipe_partition(bin_path=bin_path, partition=partition):
            yield line
        sleep(1)

    # activate sideload
    logger.info("Wiping is done, now activate sideload.")
    for line in activate_sideload(bin_path=bin_path):
        yield line
    # now flash os image
    sleep(5)
    logger.info("Sideload and install os image.")
    for line in adb_sideload(bin_path=bin_path, target=target):
        yield line
    # wipe some cache partitions
    sleep(7)
    for partition in ["dalvik", "cache"]:
        for line in run_command(f"adb shell twrp wipe {partition}", bin_path):
            yield line
        sleep(1)
        if (type(line) == bool) and not line:
            logger.error(f"Wiping {partition} failed.")
            # TODO: if this fails, a fix can be to just sideload something and then adb reboot
            for line in run_command(
                f"adb sideload {config_path.parent.joinpath(Path('helper.txt'))}",
                bin_path,
            ):
                yield line
            if (type(line) == bool) and not line:
                yield False
            break
        sleep(2)
    # finally reboot into os or to fastboot for flashing addons
    sleep(7)
    if install_addons:
        if is_ab:
            # reboot into the bootloader again
            for line in adb_reboot_bootloader(bin_path):
                yield line
            sleep(3)
            # boot to TWRP again
            for line in fastboot_flash_recovery(
                bin_path=bin_path, recovery=recovery, is_ab=is_ab
            ):
                yield line
            sleep(7)
        else:
            # if not an a/b-device just stay in twrp
            pass
    else:
        for line in adb_reboot(bin_path=bin_path):
            yield line


def adb_twrp_install_addons(bin_path: Path, addons: List[str], is_ab: bool) -> bool:
    """Flash addons through adb and twrp.

    Only works for twrp recovery.
    """
    logger.info("Install addons with twrp.")
    sleep(5)
    logger.info("Sideload and install addons.")
    for addon in addons:
        # activate sideload
        logger.info("Activate sideload.")
        for line in activate_sideload(bin_path=bin_path):
            yield line
        sleep(5)
        # now flash os image
        for line in adb_sideload(bin_path=bin_path, target=addon):
            yield line
        sleep(7)
    # finally reboot into os
    if is_ab:
        # reboot into the bootloader again
        for line in adb_reboot_bootloader(bin_path=bin_path):
            yield line
        sleep(3)
        # switch active boot partition
        for line in fastboot_switch_partition(bin_path=bin_path):
            yield line
        sleep(1)
        for line in fastboot_switch_partition(bin_path=bin_path):
            yield line
        sleep(1)
        # reboot with fastboot
        logger.info("Reboot into OS.")
        for line in fastboot_reboot(bin_path=bin_path):
            yield line
    else:
        # reboot with adb
        for line in adb_reboot(bin_path=bin_path):
            yield line


@add_logging("Switch active boot partitions.", return_if_fail=True)
def fastboot_switch_partition(bin_path: Path) -> Union[str, bool]:
    """Switch the active boot partition with fastboot."""
    for line in run_command("fastboot set_active other", bin_path):
        yield line


@add_logging("Unlock the device with fastboot and code.")
def fastboot_unlock_with_code(bin_path: Path, unlock_code: str) -> Union[str, bool]:
    """Unlock the device with fastboot and code given."""
    for line in run_command(f"fastboot oem unlock {unlock_code}", bin_path):
        yield line


@add_logging("Unlock the device with fastboot without code.")
def fastboot_unlock(bin_path: Path) -> Union[str, bool]:
    """Unlock the device with fastboot and without code."""
    for line in run_command("fastboot flashing unlock", bin_path):
        yield line


@add_logging("OEM unlocking the device with fastboot.")
def fastboot_oem_unlock(bin_path: Path) -> Union[str, bool]:
    """OEM unlock the device with fastboot and without code."""
    for line in run_command("fastboot oem unlock", bin_path):
        yield line


@add_logging("Get unlock data with fastboot")
def fastboot_get_unlock_data(bin_path: Path) -> Union[str, bool]:
    """Get the unlock data with fastboot"""
    for line in run_command("fastboot oem get_unlock_data", bin_path):
        yield line


@add_logging("Rebooting device with fastboot.")
def fastboot_reboot(bin_path: Path) -> Union[str, bool]:
    """Reboot with fastboot"""
    for line in run_command("fastboot reboot", bin_path):
        yield line


@add_logging("Flash or boot custom recovery with fastboot.")
def fastboot_flash_recovery(
    bin_path: Path, recovery: str, is_ab: bool = True
) -> Union[str, bool]:
    """Temporarily, flash custom recovery with fastboot."""
    if is_ab:
        logger.info("Boot custom recovery with fastboot.")
        for line in run_command(f"fastboot boot {recovery}", bin_path):
            yield line
    else:
        logger.info("Flash custom recovery with fastboot.")
        for line in run_command(f"fastboot flash recovery {recovery}", bin_path):
            yield line
        if (type(line) == bool) and not line:
            logger.error("Flashing recovery failed.")
            yield False
        else:
            yield True
        # reboot
        logger.info("Boot into TWRP with fastboot.")
        for line in run_command("fastboot reboot recovery", bin_path):
            yield line


def fastboot_flash_boot(bin_path: Path, recovery: str) -> bool:
    """Temporarily, flash custom recovery with fastboot to boot partition."""
    logger.info("Flash custom recovery with fastboot.")
    for line in run_command(f"fastboot flash boot {recovery}", bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Flashing recovery failed.")
        yield False
    else:
        yield True
    # reboot
    logger.info("Boot into TWRP with fastboot.")
    for line in run_command("fastboot reboot", bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Booting recovery failed.")
        yield False
    else:
        yield True


@add_logging("Flash custom recovery with heimdall.")
def heimdall_flash_recovery(bin_path: Path, recovery: str) -> Union[str, bool]:
    """Temporarily, flash custom recovery with heimdall."""
    for line in run_command(
        f"heimdall flash --no-reboot --RECOVERY {recovery}", bin_path
    ):
        yield line


def search_device(platform: str, bin_path: Path) -> Optional[str]:
    """Search for a connected device."""
    logger.info(f"Search devices on {platform} with {bin_path}...")
    try:
        # read device code
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


def check_ab_partition(platform: str, bin_path: Path) -> Optional[str]:
    """Figure out, if its an a/b-partitioned device."""
    logger.info(f"Run on {platform} with {bin_path}...")
    try:
        # check if ab device
        if platform in ("linux", "darwin"):
            output = check_output(
                [
                    str(bin_path.joinpath(Path("adb"))),
                    "shell",
                    "getprop",
                    "|",
                    "grep",
                    "ro.boot.slot_suffix",
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
                    "ro.boot.slot_suffix",
                ],
                stderr=STDOUT,
                shell=True,
            ).decode()
        else:
            raise Exception(f"Unknown platform {platform}.")
        logger.info(output)
        logger.info("This is an a/b-partitioned device.")
        return True
    except CalledProcessError:
        logger.info("This is not an a/b-partitioned device.")
        return False
