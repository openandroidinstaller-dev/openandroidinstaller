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
from typing import Optional, Union, Generator, Callable

from loguru import logger


TerminalResponse = Generator[Union[str, bool], None, None]


PLATFORM = sys.platform


def run_command(
    full_command: str,
    bin_path: Path,
    target: Optional[Union[str, Path]] = None,
    enable_logging: bool = True,
) -> TerminalResponse:
    """Run a command with a tool (adb, fastboot, heimdall)."""
    yield f"${full_command}"
    # split the command and extract the tool part
    tool, *command = shlex.split(full_command)
    if tool not in ["adb", "fastboot", "heimdall"]:
        raise Exception(f"Unknown tool {tool}. Use adb, fastboot or heimdall.")
    if PLATFORM == "win32":
        command_list = [str(bin_path.joinpath(Path(f"{tool}"))) + ".exe"] + command
        # prevent Windows from opening terminal windows
        si = subprocess.STARTUPINFO()  # type: ignore
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW  # type: ignore
    else:
        command_list = [str(bin_path.joinpath(Path(f"{tool}")))] + command
        si = None
    if enable_logging:
        logger.info(f"Run command: {command_list}")
    if target:
        command_list.append(f"{target}")
    # run the command
    with subprocess.Popen(
        command_list,
        stdout=PIPE,
        stderr=STDOUT,
        bufsize=1,
        universal_newlines=True,
        startupinfo=si,
    ) as p:
        for line in p.stdout:  # type: ignore
            if enable_logging:
                logger.info(line.strip())
            yield line.strip()

    # finally return if the command was successful
    yield p.returncode == 0


def add_logging(step_desc: str, return_if_fail: bool = False) -> Callable:
    """Logging decorator to wrap functions that yield lines.

    Logs the `step_desc`.
    """

    def logging_decorator(func) -> Callable:
        def logging(*args, **kwargs) -> TerminalResponse:
            logger.info(f"{step_desc} - Parameters: {kwargs}")
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
def adb_reboot(bin_path: Path) -> TerminalResponse:
    """Run adb reboot on the device and return success."""
    for line in run_command("adb reboot", bin_path):
        yield line


@add_logging("Rebooting device into bootloader with adb.", return_if_fail=True)
def adb_reboot_bootloader(bin_path: Path) -> TerminalResponse:
    """Reboot the device into bootloader and return success."""
    for line in run_command("adb reboot bootloader", bin_path):
        yield line
    # wait for the bootloader to become available
    for line in fastboot_wait_for_bootloader(bin_path=bin_path):
        yield line


@add_logging("Rebooting device into download mode with adb.")
def adb_reboot_download(bin_path: Path) -> TerminalResponse:
    """Reboot the device into download mode of samsung devices and return success."""
    for line in run_command("adb reboot download", bin_path):
        yield line
    yield heimdall_wait_for_download_available(bin_path=bin_path)


@add_logging("Sideload the target to device with adb.")
def adb_sideload(bin_path: Path, target: str) -> TerminalResponse:
    """Sideload the target to device and return success."""
    for line in run_command("adb sideload", target=target, bin_path=bin_path):
        yield line


@add_logging("Activate sideloading in TWRP.", return_if_fail=True)
def activate_sideload(bin_path: Path) -> TerminalResponse:
    """Activate sideload with adb shell in twrp."""
    for line in run_command("adb shell twrp sideload", bin_path):
        yield line
    for line in adb_wait_for_sideload(bin_path=bin_path):
        yield line


@add_logging("Wait for device")
def adb_wait_for_device(bin_path: Path) -> TerminalResponse:
    """Use adb to wait for the device to become available."""
    for line in run_command("adb wait-for-device", bin_path):
        yield line


@add_logging("Wait for recovery")
def adb_wait_for_recovery(bin_path: Path) -> TerminalResponse:
    """Use adb to wait for the recovery to become available."""
    for line in run_command("adb wait-for-recovery", bin_path):
        yield line


@add_logging("Wait for sideload")
def adb_wait_for_sideload(bin_path: Path) -> TerminalResponse:
    """Use adb to wait for the sideload to become available."""
    for line in run_command("adb wait-for-sideload", bin_path):
        yield line


def adb_twrp_copy_partitions(bin_path: Path, config_path: Path) -> TerminalResponse:
    # some devices like one plus 6t or motorola moto g7 power need the partitions copied to prevent a hard brick
    logger.info("Sideload copy_partitions script with adb.")
    # activate sideload
    for line in activate_sideload(bin_path):
        yield line
    # now sideload the script
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
    # Copy partitions end #
    yield True


@add_logging("Perform a factory reset with adb and twrp.", return_if_fail=True)
def adb_twrp_format_data(bin_path: Path) -> TerminalResponse:
    """Perform a factory reset with twrp and adb."""
    for line in run_command("adb shell twrp format data", bin_path):
        yield line


@add_logging("Wipe the selected partition with adb and twrp.", return_if_fail=True)
def adb_twrp_wipe_partition(bin_path: Path, partition: str) -> TerminalResponse:
    """Perform a factory reset with twrp and adb."""
    for line in run_command(f"adb shell twrp wipe {partition}", bin_path):
        yield line


def adb_twrp_wipe_and_install(
    bin_path: Path,
    target: str,
    config_path: Path,
    is_ab: bool,
    install_addons=True,
    recovery: Optional[str] = None,
) -> TerminalResponse:
    """Wipe and format data with twrp, then flash os image with adb.

    Only works for twrp recovery.
    """
    logger.info("Wipe and format data with twrp, then install os image.")
    for line in adb_wait_for_recovery(bin_path):
        yield line

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
    logger.info("Sideload and install os image.")
    for line in adb_sideload(bin_path=bin_path, target=target):
        yield line
    # wipe some cache partitions
    sleep(7)
    for partition in ["dalvik", "cache"]:
        for line in run_command(f"adb shell twrp wipe {partition}", bin_path):
            yield line
        sleep(3)
        if (type(line) == bool) and not line:
            logger.error(f"Wiping {partition} failed.")
            # TODO: if this fails, a fix can be to just sideload something and then adb reboot
            for line in adb_sideload(
                target=f"{config_path.parent.joinpath(Path('helper.txt'))}",
                bin_path=bin_path,
            ):
                yield line
            sleep(1)
            if (type(line) == bool) and not line:
                yield False
            break
        sleep(2)
    # finally reboot into os or to fastboot for flashing addons
    for line in adb_wait_for_recovery(bin_path):
        yield line
    if install_addons:
        if is_ab:
            # reboot into the bootloader again
            for line in adb_reboot_bootloader(bin_path):
                yield line
            sleep(3)
            # boot to TWRP again
            for line in fastboot_boot_recovery(
                bin_path=bin_path, recovery=recovery, is_ab=is_ab
            ):
                yield line
        else:
            # if not an a/b-device just stay in twrp
            pass
    else:
        for line in adb_reboot(bin_path=bin_path):
            yield line


def adb_twrp_install_addon(
    bin_path: Path, addon_path: str, is_ab: bool
) -> TerminalResponse:
    """Flash addon through adb and twrp.

    Only works for twrp recovery.
    """
    logger.info(f"Install addon {addon_path} with twrp.")
    sleep(0.5)
    if is_ab:
        adb_wait_for_recovery(bin_path=bin_path)
    # activate sideload
    logger.info("Activate sideload.")
    for line in activate_sideload(bin_path=bin_path):
        yield line
    logger.info("Sideload and install addon.")
    # now flash the addon
    for line in adb_sideload(bin_path=bin_path, target=addon_path):
        yield line
    logger.info("done.")


def adb_twrp_finish_install_addons(bin_path: Path, is_ab: bool) -> TerminalResponse:
    """Finish the process of flashing addons with TWRP and reboot.

    Only works for twrp recovery.
    """
    sleep(3)
    for line in adb_wait_for_recovery(bin_path):
        yield line
    # finally reboot into os
    if is_ab:
        logger.info("Switch partitions on a/b-partitioned device.")
        # reboot into the bootloader again
        for line in adb_reboot_bootloader(bin_path=bin_path):
            yield line
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
        logger.info("Reboot into OS.")
        for line in adb_reboot(bin_path=bin_path):
            yield line


@add_logging("Wait for bootloader")
def fastboot_wait_for_bootloader(bin_path: Path) -> TerminalResponse:
    """Use adb to wait for the bootloader to become available."""
    for line in run_command("fastboot devices", bin_path):
        yield line


@add_logging("Switch active boot partitions.", return_if_fail=True)
def fastboot_switch_partition(bin_path: Path) -> TerminalResponse:
    """Switch the active boot partition with fastboot."""
    for line in run_command("fastboot set_active other", bin_path):
        yield line


@add_logging("Unlock the device with fastboot and code.")
def fastboot_unlock_with_code(bin_path: Path, unlock_code: str) -> TerminalResponse:
    """Unlock the device with fastboot and code given."""
    for line in run_command(f"fastboot oem unlock {unlock_code}", bin_path):
        yield line


@add_logging("Unlock the device with fastboot without code.")
def fastboot_unlock(bin_path: Path) -> TerminalResponse:
    """Unlock the device with fastboot and without code."""
    for line in run_command("fastboot flashing unlock", bin_path):
        yield line


@add_logging("OEM unlocking the device with fastboot.")
def fastboot_oem_unlock(bin_path: Path) -> TerminalResponse:
    """OEM unlock the device with fastboot and without code."""
    for line in run_command("fastboot oem unlock", bin_path):
        yield line


@add_logging("Get unlock data with fastboot")
def fastboot_get_unlock_data(bin_path: Path) -> TerminalResponse:
    """Get the unlock data with fastboot"""
    for line in run_command("fastboot oem get_unlock_data", bin_path):
        yield line


@add_logging("Rebooting device with fastboot.")
def fastboot_reboot(bin_path: Path) -> TerminalResponse:
    """Reboot with fastboot"""
    for line in run_command("fastboot reboot", bin_path):
        yield line


@add_logging("Boot custom recovery with fastboot.")
def fastboot_boot_recovery(
    bin_path: Path, recovery: str, is_ab: bool = True
) -> TerminalResponse:
    """Temporarily, boot custom recovery with fastboot."""
    logger.info("Boot custom recovery with fastboot.")
    for line in run_command("fastboot boot", target=f"{recovery}", bin_path=bin_path):
        yield line
    if not is_ab:
        if (type(line) == bool) and not line:
            logger.error("Booting recovery failed.")
            yield False
        else:
            yield True
    for line in adb_wait_for_recovery(bin_path=bin_path):
        yield line


def fastboot_flash_boot(bin_path: Path, recovery: str) -> TerminalResponse:
    """Temporarily, flash custom recovery with fastboot to boot partition."""
    logger.info("Flash custom recovery with fastboot.")
    for line in run_command(
        "fastboot flash boot", target=f"{recovery}", bin_path=bin_path
    ):
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
    for line in adb_wait_for_recovery(bin_path=bin_path):
        yield line
    if (type(line) == bool) and not line:
        logger.error("Booting recovery failed.")
        yield False
    else:
        yield True


def heimdall_wait_for_download_available(bin_path: Path) -> bool:
    """Use heimdall detect to wait for download mode to become available on the device."""
    logger.info("Wait for download mode to become available.")
    while True:
        sleep(1)
        for line in run_command("heimdall detect", bin_path=bin_path):
            if (type(line) == bool) and line:
                return True


@add_logging("Flash custom recovery with heimdall.")
def heimdall_flash_recovery(bin_path: Path, recovery: str) -> TerminalResponse:
    """Temporarily, flash custom recovery with heimdall."""
    for line in run_command(
        "heimdall flash --no-reboot --RECOVERY", target=f"{recovery}", bin_path=bin_path
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
