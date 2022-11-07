"""This file contains some utility functions."""

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

import zipfile
from typing import Optional

import requests
from installer_config import Step
from loguru import logger


def get_download_link(devicecode: str) -> Optional[str]:
    """Check if a lineageOS version for this device exists on lineageosroms.com and return the respective download link."""
    url = f"https://download.lineageos.org/{devicecode.lower()}"
    try:
        logger.info(f"Checking {url}")
        # Get Url
        res = requests.get(url)
        # if the request succeeds
        if res.status_code == 200:
            logger.info(f"{url} exists.")
            return url
        else:
            logger.info(f"{url} doesn't exist, status_code: {res.status_code}")
            return
    except requests.exceptions.RequestException as e:
        logger.info(f"{url} doesn't exist, error: {e}")
        return


def image_recovery_works_with_device(
    device_code: str, image_path: str, recovery_path: str
) -> bool:
    """Determine if an image and recovery works for the given device.

    BEWARE: THE RECOVERY PART IS STILL VERY BASIC!
    """
    with zipfile.ZipFile(image_path) as image_zip:
        with image_zip.open(
            "META-INF/com/android/metadata", mode="r"
        ) as image_metadata:
            metadata = image_metadata.readlines()
            supported_devices = str(metadata[-1]).split("=")[-1][:-3].split(",")
            logger.info(f"Image works with device: {supported_devices}")

            if (device_code in supported_devices) and (
                device_code in recovery_path.split("/")[-1]
            ):
                logger.info("Device supported by the image and recovery.")
                return True
    return False
