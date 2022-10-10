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

from typing import Optional

import requests
from loguru import logger


def get_download_link(devicecode: str) -> Optional[str]:
    """Check if a lineageOS version for this device exists on lineageosroms.com and return the respective download link."""
    url = f"https://lineageosroms.com/{devicecode}/"
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


class AppState:
    """Container class to store all kinds of state."""

    def __init__(self):
        self.steps = None
