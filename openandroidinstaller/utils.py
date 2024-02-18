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
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import requests
from loguru import logger


class CompatibilityStatus(Enum):
    """Enum for the compatibility status of a device."""

    UNKNOWN = 0
    COMPATIBLE = 1
    INCOMPATIBLE = 2


@dataclass
class CheckResult:
    """Dataclass for the result of a check.

    Attributes:
        status: Compatibility status of the device.
        message: Message to be displayed to the user.
    """

    status: CompatibilityStatus
    message: str


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


def retrieve_image_metadata(image_path: str) -> dict:
    """Retrieve metadata from the selected image.

    Args:
        image_path: Path to the image file.

    Returns:
        Dictionary containing the metadata.
    """
    metapath = "META-INF/com/android/metadata"
    try:
        with zipfile.ZipFile(image_path) as image_zip:
            with image_zip.open(metapath, mode="r") as image_metadata:
                metadata = image_metadata.readlines()
            metadata_dict = {}
            for line in metadata:
                metadata_dict[line[: line.find(b"=")].decode("utf-8")] = line[
                    line.find(b"=") + 1 : -1
                ].decode("utf-8")
            logger.info(f"Metadata retrieved from image {image_path.split('/')[-1]}.")
            return metadata_dict
    except zipfile.BadZipFile as e:
        raise e
    except (FileNotFoundError, KeyError):
        logger.error(
            f"Metadata file {metapath} not found in {image_path.split('/')[-1]}."
        )
        return dict()


def image_sdk_level(image_path: str) -> int:
    """Determine Android version of the selected image.

    Examples:
        Android 10: 29
        Android 11: 30
        Android 12: 31
        Android 12.1: 32
        Android 13: 33

    Args:
        image_path: Path to the image file.

    Returns:
        Android version as integer.
    """
    try:
        metadata = retrieve_image_metadata(image_path)
        sdk_level = metadata["post-sdk-level"]
        logger.info(f"Android version of {image_path}: {sdk_level}")
        return int(sdk_level)
    except (ValueError, TypeError, KeyError, zipfile.BadZipFile) as e:
        logger.error(f"Could not determine Android version of {image_path}. Error: {e}")
        return -1


def image_works_with_device(
    supported_device_codes: List[str], image_path: str
) -> CheckResult:
    """Determine if an image works for the given device.

    Args:
        supported_device_codes: List of supported device codes from the config file.
        image_path: Path to the image file.

    Returns:
        CheckResult object containing the compatibility status and a message.
    """
    try:
        metadata = retrieve_image_metadata(image_path)
        supported_devices = metadata["pre-device"].split(",")
        logger.info(f"Image works with the following device(s): {supported_devices}")
        if any(code in supported_devices for code in supported_device_codes):
            logger.success("Device supported by the selected image.")
            return CheckResult(
                CompatibilityStatus.COMPATIBLE,
                "Device supported by the selected image.",
            )
        else:
            logger.error(f"Image file {image_path.split('/')[-1]} is not supported.")
            return CheckResult(
                CompatibilityStatus.INCOMPATIBLE,
                f"Image file {image_path.split('/')[-1]} is not supported by device code.",
            )
    except zipfile.BadZipFile:
        logger.error("Selected image is not a zip file.")
        return CheckResult(
            CompatibilityStatus.INCOMPATIBLE,
            f"Selected image {image_path.split('/')[-1]} is not a zip file.",
        )
    except KeyError:
        logger.error(
            f"Could not determine supported devices for {image_path.split('/')[-1]}."
        )
        return CheckResult(
            CompatibilityStatus.UNKNOWN,
            f"Could not determine supported devices for {image_path.split('/')[-1]}. Missing metadata file? You may try to flash the image anyway.",
        )


def recovery_works_with_device(
    supported_device_codes: List[str], recovery_path: str
) -> CheckResult:
    """Determine if a recovery works for the given device.

    BEWARE: THE RECOVERY PART IS STILL VERY BASIC!

    Args:
        supported_device_codes: List of supported device codes from the config file.
        recovery_path: Path to the recovery file.

    Returns:
        CheckResult object containing the compatibility status and a message.
    """
    recovery_file_name = recovery_path.split("/")[-1]
    if any(code in recovery_file_name for code in supported_device_codes) and (
        "twrp" in recovery_file_name
    ):
        logger.success("Device supported by the selected recovery.")
        return CheckResult(
            CompatibilityStatus.COMPATIBLE, "Device supported by the selected recovery."
        )
    else:
        logger.error(f"Recovery file {recovery_file_name} is not supported.")
        return CheckResult(
            CompatibilityStatus.INCOMPATIBLE,
            f"Recovery file {recovery_file_name} is not supported by device code in file name.",
        )
