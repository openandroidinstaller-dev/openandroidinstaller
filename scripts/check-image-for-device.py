"""Script to check if a given lineageOS image works for a connected device."""

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

from os import device_encoding
from subprocess import STDOUT, check_output
from typing import Dict


def get_device_info() -> Dict[str, str]:
    """Read the device properties with adb."""
    # read properties
    device_properties = check_output(
        ["adb", "shell", "getprop"], stderr=STDOUT
    ).decode()
    # clean and structure the properties into dict
    properties_dict = dict(
        [
            prop.replace("[", "").replace("]", "").split(":", 1)
            for prop in device_properties.split("\n")
            if len(prop) > 2
        ]
    )
    # filter down to some relevant properties used for identifying the device
    relevant_keys = ("ro.product.manufacturer", "ro.product.model", "ro.product.name")
    return {key: properties_dict[key].strip() for key in relevant_keys}


def image_works(image_path: str, device_code: str) -> bool:
    """Determine if the image works or not."""
    raw_text = check_output(["cat", f"{image_path}"], stderr=STDOUT).decode(
        encoding="latin"
    )
    return device_code in raw_text


if __name__ == "__main__":
    device_info = get_device_info()
    print(device_info)

    # image_path = "images/samsung-galaxy-a3/lineage-16.0-20190908-UNOFFICIAL-a3y17lte.zip"
    image_path = (
        "images/samsung-galaxy-a3/lineage-17.1-20200830-UNOFFICIAL-a3y17lte.zip"
    )
    works = image_works(image_path, device_code=device_info["ro.product.name"])
    if works:
        print("This image works for your device!")
    else:
        print("This image will not work for your device...")
