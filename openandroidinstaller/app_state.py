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
import copy
from pathlib import Path
from typing import List, Optional

from installer_config import Step, _load_config
from loguru import logger


class AppState:
    """Container class to store the state of the application."""

    def __init__(
        self,
        platform: str,
        config_path: Path,
        bin_path: Path,
        test: bool = False,
        test_config: Optional[str] = None,
    ):
        self.platform = platform
        self.config_path = config_path
        self.bin_path = bin_path
        self.test = test
        self.test_config = test_config

        # store state
        self.unlock_bootloader = True
        self.flash_recovery = True

        # placeholders
        self.advanced = False
        self.install_addons = False
        self.addon_paths = []
        self.config = None
        self.image_path = None
        self.recovery_path = None
        self.dtbo_path = None
        self.vbmeta_path = None
        self.super_empty_path = None
        self.vendor_boot_path = None

        # store views
        self.default_views: List = []
        self.addon_views: List = []
        self.final_default_views: List = []

    def add_default_views(self, views: List):
        """Add default views to store"""
        self.default_views.extend(views)

    def add_addon_views(self, views: List):
        """Add addon views to store"""
        self.addon_views.extend(views)

    def add_final_default_views(self, views: List):
        """Add final default views to store"""
        self.final_default_views.extend(views)

    def load_config(self, device_code: str):
        """Load the config from file to state by device code."""
        self.config = _load_config(device_code, self.config_path)
        if self.config:
            self.steps = copy.deepcopy(self.config.unlock_bootloader) + copy.deepcopy(
                self.config.boot_recovery
            )

    def toggle_flash_unlock_bootloader(self):
        """Toggle flashing of unlock bootloader."""
        self.unlock_bootloader = not self.unlock_bootloader
        if self.unlock_bootloader:
            logger.info("Enabled unlocking the bootloader again.")
            self.steps = copy.deepcopy(self.config.unlock_bootloader)
        else:
            logger.info("Skipping bootloader unlocking.")
            self.steps = []
        # if the recovery is already flashed, skip flashing it again
        if self.flash_recovery:
            self.steps += copy.deepcopy(self.config.boot_recovery)
        else:
            self.steps = [
                Step(
                    title="Boot custom recovery",
                    type="confirm_button",
                    content="If you already flashed TWRP, boot into it by pressing 'Confirm and run'. Otherwise restart the process. Once your phone screen looks like the picture on the left, continue.",
                    command="adb_reboot_recovery",
                    img="twrp-start.jpeg",
                )
            ]

    def toggle_flash_recovery(self):
        """Toggle flashing of recovery."""
        self.flash_recovery = not self.flash_recovery
        if self.unlock_bootloader:
            self.steps = copy.deepcopy(self.config.unlock_bootloader)
        else:
            self.steps = []
        if self.flash_recovery:
            logger.info("Enabled flashing recovery again.")
            self.steps += copy.deepcopy(self.config.boot_recovery)
        else:
            logger.info("Skipping flashing recovery.")
            self.steps = [
                Step(
                    title="Boot custom recovery",
                    type="call_button",
                    content="If you already flashed TWRP, boot into it by pressing 'Confirm and run'. Otherwise restart the process. Once your phone screen looks like the picture on the left, continue.",
                    command="adb_reboot_recovery",
                    img="twrp-start.jpeg",
                )
            ]
