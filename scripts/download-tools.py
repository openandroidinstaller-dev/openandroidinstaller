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

import py7zr
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


def download_libusb(platform: str):
    """Download libusb-1.0, extract the 7z and save to file."""
    logger.info(f"Download libusb-1.0 for {platform}...")
    url = "https://github.com/libusb/libusb/releases/download/v1.0.24/libusb-1.0.24.7z"
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)

    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("libusb-windows")).resolve()
    logger.info(download_path)
    with py7zr.SevenZipFile(BytesIO(response.content)) as file:
        file.extractall(download_path.name)
    logger.info("DONE.")


def move_files_to_lib(platform: str):
    """Move files to the expected path in the openandroidinstaller package."""
    target_path = Path(os.sep.join(["openandroidinstaller", "bin"]), exist_ok=True)
    logger.info(f"Move executables to {target_path}...")
    # move the platformtools
    pt_path = (
        Path(__file__)
        .parent.joinpath(Path(os.sep.join(["..", "tools", "platform-tools"])))
        .resolve()
    )
    logger.info(pt_path)
    pt_target_path = (
        Path(__file__)
        .parent.joinpath(Path(os.sep.join(["..", "openandroidinstaller", "bin"])))
        .resolve()
    )
    logger.info(pt_target_path)
    pt_path.rename(pt_target_path)
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
    # move libusb
    libusb_path = (
        Path(__file__)
        .parent.joinpath(
            Path(
                os.sep.join(
                    ["..", "libusb-windows", "MinGW32", "dll", "libusb-1.0.dll"]
                )
            )
        )
        .resolve()
    )
    logger.info(libusb_path)
    libusb_target_path = (
        Path(__file__)
        .parent.joinpath(
            Path(os.sep.join(["..", "openandroidinstaller", "bin", "libusb-1.0.dll"]))
        )
        .resolve()
    )
    logger.info(libusb_target_path)
    libusb_path.rename(libusb_target_path)
    logger.info("DONE.")
    # make executable
    logger.info("Allow the executables to be executed.")
    for executable_name in ["fastboot", "adb", "mke2fs", "heimdall"]:
        if platform == "win32":
            (pt_target_path / (executable_name + ".exe")).chmod(0o755)
        else:
            (pt_target_path / executable_name).chmod(0o755)
    logger.info("DONE.")


def main(platform: str):
    logger.info(f"Run downloads for {platform} ...")
    download_adb_fastboot(platform=platform)
    download_heimdall(platform=platform)
    download_libusb(platform=platform)
    move_files_to_lib(platform=platform)


if __name__ == "__main__":
    main(platform=sys.platform)
