"""This file contains a class and function to manage the app state over various steps."""

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

from flet import ProgressBar
from installer_config import _load_config


class AppState:
    """Container class to store the state of the application."""

    def __init__(
        self,
        platform: str,
        config_path: Path,
        bin_path: Path,
        test: bool = False,
        test_config: str = None,
    ):
        self.platform = platform
        self.config_path = config_path
        self.bin_path = bin_path
        self.test = test
        self.test_config = test_config

        # placeholders
        self.advanced = False
        self.config = None
        self.image_path = None
        self.recovery_path = None

        # is this still needed?
        self.steps = None

    def load_config(self, device_code: str):
        """Load the config from file to state by device code."""
        self.config = _load_config(device_code, self.config_path)
        if self.config:
            self.steps = (
                self.config.unlock_bootloader
                + self.config.flash_recovery
                + self.config.install_os
            )