"""Basic script to get adb and fastboot.

Inspired by: https://gitlab.com/ubports/installer/android-tools-bin/-/blob/master/build.js
"""

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

import os
import sys
import zipfile
from io import BytesIO
from pathlib import Path

import requests
from loguru import logger


def download_adb_fastboot(platform: str):
    """Download adb and fastboot executable from dl.google.com, extract the zip and save to file."""
    if platform == "win32":
        platform = "windows"
    logger.info(f"Download adb and fastboot for {platform}...")
    url = (
        f"https://dl.google.com/android/repository/platform-tools-latest-{platform}.zip"
    )
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)

    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("tools")).resolve()
    logger.info(download_path)
    file = zipfile.ZipFile(BytesIO(response.content))
    file.extractall(download_path.name)
    logger.info("DONE.")


def download_heimdall(platform: str):
    """Download heimdall executable from ubuntu.com, extract the zip and save to file."""
    logger.info(f"Download heimdall for {platform}...")
    url = f"https://people.ubuntu.com/~neothethird/heimdall-{platform}.zip"
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)

    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("heimdall")).resolve()
    logger.info(download_path)
    file = zipfile.ZipFile(BytesIO(response.content))
    file.extractall(download_path.name)
    logger.info("DONE.")


def move_files_to_lib(platform: str):
    """Move files to the expected path in the openandroidinstaller package."""
    target_path = Path(os.sep.join(["openandroidinstaller", "bin"]), exist_ok=True)
    logger.info(f"Move executables to {target_path}...")
    target_path.mkdir(exist_ok=True)
    # move adb
    adb_path = (
        Path(__file__)
        .parent.joinpath(Path(os.sep.join(["..", "tools", "platform-tools", "adb"])))
        .resolve()
    )
    logger.info(adb_path)
    adb_target_path = (
        Path(__file__)
        .parent.joinpath(
            Path(os.sep.join(["..", "openandroidinstaller", "bin", "adb"]))
        )
        .resolve()
    )
    if platform == "win32":
        adb_path = adb_path.parents[0] / "adb.exe"
        adb_target_path = adb_target_path.parents[0] / "adb.exe"
    logger.info(adb_target_path)
    adb_path.rename(adb_target_path)
    # if windows, also move dll
    if platform == "win32":
        adb_path = adb_path.parents[0] / "AdbWinApi.dll"
        adb_target_path = adb_target_path.parents[0] / "AdbWinApi.dll"
        logger.info(adb_target_path)
        adb_path.rename(adb_target_path)
    # move fastboot
    fb_path = (
        Path(__file__)
        .parent.joinpath(
            Path(os.sep.join(["..", "tools", "platform-tools", "fastboot"]))
        )
        .resolve()
    )
    fb_target_path = (
        Path(__file__)
        .parent.joinpath(
            Path(os.sep.join(["..", "openandroidinstaller", "bin", "fastboot"]))
        )
        .resolve()
    )
    if platform == "win32":
        fb_path = fb_path.parents[0] / "fastboot.exe"
        fb_target_path = fb_target_path.parents[0] / "fastboot.exe"
    fb_path.rename(fb_target_path)
    # move heimdall
    hd_path = (
        Path(__file__)
        .parent.joinpath(Path(os.sep.join(["..", "heimdall", "heimdall"])))
        .resolve()
    )
    hd_target_path = (
        Path(__file__)
        .parent.joinpath(
            Path(os.sep.join(["..", "openandroidinstaller", "bin", "heimdall"]))
        )
        .resolve()
    )
    if platform == "win32":
        hd_path = hd_path.parents[0] / "heimdall.exe"
        hd_target_path = hd_target_path.parents[0] / "heimdall.exe"
    hd_path.rename(hd_target_path)
    logger.info("DONE.")
    # make executable
    logger.info("Allow the executables to be executed.")
    adb_target_path.chmod(0o755)
    fb_target_path.chmod(0o755)
    hd_target_path.chmod(0o755)
    logger.info("DONE.")


def main(platform: str):
    logger.info(f"Run downloads for {platform} ...")
    download_adb_fastboot(platform=platform)
    download_heimdall(platform=platform)
    move_files_to_lib(platform=platform)


if __name__ == "__main__":
    main(platform=sys.platform)
