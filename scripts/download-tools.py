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

import requests
from pathlib import Path
import zipfile
from io import BytesIO
from loguru import logger
import click


def download_adb_fastboot(platform: str):
    """Download adb and fastboot executable from dl.google.com, extract the zip and save to file."""
    logger.info(f"Download adb and fastboot for {platform}...")
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{platform}.zip"
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)
    # Split URL to get the file name
    filename = url.split('/')[-1]
 
    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("tools")).resolve()
    file = zipfile.ZipFile(BytesIO(response.content))
    file.extractall(download_path.name)
    logger.info("DONE.")


def download_heimdall(platform: str):
    """Download heimdall executable from ubuntu.com, extract the zip and save to file."""
    logger.info(f"Download heimdall for {platform}...")
    url = f"https://people.ubuntu.com/~neothethird/heimdall-{platform}.zip"
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)
    # Split URL to get the file name
    filename = url.split('/')[-1]
 
    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("heimdall")).resolve()
    file = zipfile.ZipFile(BytesIO(response.content))
    file.extractall(download_path.name)
    logger.info("DONE.")


def move_files_to_lib():
    """Move files to the expected path in the openandroidinstaller package."""
    target_path = Path("openandroidinstaller/bin", exist_ok=True)
    logger.info(f"Move executables to {target_path}...")
    target_path.mkdir(exist_ok=True)
    # move adb
    adb_path = Path(__file__).parent.joinpath(Path("../tools/platform-tools/adb")).resolve()
    adb_target_path = Path(__file__).parent.joinpath(Path("../openandroidinstaller/bin/adb")).resolve()
    adb_path.rename(adb_target_path)
    # move fastboot
    fb_path = Path(__file__).parent.joinpath(Path("../tools/platform-tools/fastboot")).resolve()
    fb_target_path = Path(__file__).parent.joinpath(Path("../openandroidinstaller/bin/fastboot")).resolve()
    fb_path.rename(fb_target_path)
    # move heimdall
    hd_path = Path(__file__).parent.joinpath(Path("../heimdall/heimdall")).resolve()
    hd_target_path = Path(__file__).parent.joinpath(Path("../openandroidinstaller/bin/heimdall")).resolve()
    hd_path.rename(hd_target_path)
    logger.info("DONE.")
    # make executable
    logger.info("Allow the executables to be executed.")
    adb_target_path.chmod(0o755)
    fb_target_path.chmod(0o755)
    hd_target_path.chmod(0o755)
    logger.info("DONE.")
    
@click.command()
@click.option("--platform", help="On which platform should the tools work?", default="linux")
def main(platform: str):
    download_adb_fastboot(platform=platform)
    download_heimdall(platform=platform)
    move_files_to_lib()


if __name__ == "__main__":
    main()