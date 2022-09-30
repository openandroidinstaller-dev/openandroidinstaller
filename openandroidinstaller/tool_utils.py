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

from pathlib import Path
from subprocess import STDOUT, CalledProcessError, call, check_output
from typing import Optional

import regex as re
from loguru import logger


def call_tool_with_command(command: str, bin_path: Path) -> bool:
    """Call an executable with a specific command."""
    command = re.sub(r"^adb", str(bin_path.joinpath(Path("adb"))), command)
    command = re.sub(r"^fastboot", str(bin_path.joinpath(Path("fastboot"))), command)
    command = re.sub(r"^heimdall", str(bin_path.joinpath(Path("heimdall"))), command)

    logger.info(f"Run command: {command}")
    res = call(f"{command}", shell=True)
    if res == 0:
        logger.info("Success.")
        return True
    logger.info(f"Command {command} failed.")
    return False


def search_device(platform: str, bin_path: Path) -> Optional[str]:
    """Search for a connected device."""
    logger.info(f"Search devices on {platform} with {bin_path}...")
    try:
        # read device properties
        # TODO: This is not windows ready...
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
        elif platform == "windows":
            output = check_output(
                [
                    str(bin_path.joinpath(Path("adb"))),
                    "shell",
                    "getprop",
                    "|",
                    "findstr",
                    "ro.product.device",
                ],
                stderr=STDOUT,
            ).decode()
        else:
            raise Exception(f"Unknown platform {platform}.")
        return output.split("[")[-1][:-2].strip()
    except CalledProcessError:
        logger.info(f"Did not detect a device.")
        return None
