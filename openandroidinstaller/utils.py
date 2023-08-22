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
from typing import Optional, List

import requests
from loguru import logger


def get_download_link(devicecode: str) -> Optional[str]:
    """Check if a lineageOS version for this device exists on download.lineageos.com and return the respective download link."""
    url = f"https://download.lineageos.org/api/v2/devices/{devicecode}"
    try:
        logger.info(f"Checking {url}")
        # Get Url
        res = requests.get(url, timeout=5)
        # if the request succeeds
        if res.status_code == 200:
            download_url = f"https://download.lineageos.org/devices/{devicecode}/builds"
            logger.info(f"{download_url} exists.")
            return download_url
        else:
            logger.info(f"{url} doesn't exist, status_code: {res.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"{url} doesn't exist, error: {e}")
        return None


def image_works_with_device(supported_device_codes: List[str], image_path: str) -> bool:
    """Determine if an image works for the given device.

    Args:
        supported_device_codes: List of supported device codes from the config file.
        image_path: Path to the image file.

    Returns:
        True if the image works with the device, False otherwise.
    """
    with zipfile.ZipFile(image_path) as image_zip:
        with image_zip.open(
            "META-INF/com/android/metadata", mode="r"
        ) as image_metadata:
            metadata = image_metadata.readlines()
            supported_devices = str(metadata[-1]).split("=")[-1][:-3].split(",")
            logger.info(f"Image works with device: {supported_devices}")

            if any(code in supported_devices for code in supported_device_codes):
                logger.success("Device supported by the selected image.")
                return True
            else:
                logger.error(
                    f"Image file {image_path.split('/')[-1]} is not supported."
                )
                return False


def image_sdk_level(image_path: str) -> int:
    """Determine Android version of the selected image.

    Example:
        Android 13: 33
    """
    with zipfile.ZipFile(image_path) as image_zip:
        with image_zip.open(
            "META-INF/com/android/metadata", mode="r"
        ) as image_metadata:
            metadata = image_metadata.readlines()
            for line in metadata:
                if b"sdk-level" in line:
                    return int(line[line.find(b"=") + 1 : -1].decode("utf-8"))
    return 0


def recovery_works_with_device(
    supported_device_codes: List[str], recovery_path: str
) -> bool:
    """Determine if a recovery works for the given device.

    BEWARE: THE RECOVERY PART IS STILL VERY BASIC!

    Args:
        supported_device_codes: List of supported device codes from the config file.
        recovery_path: Path to the recovery file.

    Returns:
        True if the recovery works with the device, False otherwise.
    """
    recovery_file_name = recovery_path.split("/")[-1]
    if any(code in recovery_file_name for code in supported_device_codes) and (
        "twrp" in recovery_file_name
    ):
        logger.success("Device supported by the selected recovery.")
        return True
    else:
        logger.error(f"Recovery file {recovery_file_name} is not supported.")
        return False
