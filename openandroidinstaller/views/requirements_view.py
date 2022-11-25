"""Contains the requirements view."""

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

from loguru import logger
from typing import Callable
from flet import (
    Checkbox,
    Card,
    Column,
    Container,
    Divider,
    ElevatedButton,
    Markdown,
    Row,
    Text,
    icons,
)

from views import BaseView
from app_state import AppState
from widgets import get_title


class RequirementsView(BaseView):
    """View to display requirements and ask for confirmation."""

    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state, image="requirements-default.png")
        self.on_confirm = on_confirm

    def build(self):
        self.continue_button = ElevatedButton(
            "Continue",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )

        # build up the main view
        self.right_view.controls.extend(
            [
                get_title("Check the Requirements"),
                Text(
                    "Before continuing you need to check some requirements to progress. Please read the instructions and check the boxes if everything is fine."
                ),
                Divider(),
            ]
        )
        self.checkboxes = []

        def enable_continue_button(e):
            """Enable the continue button if all checkboxes are ticked."""
            for checkbox in self.checkboxes:
                if not checkbox.value:
                    self.continue_button.disabled = True
                    return
            logger.info("All requirements ticked. Allow to continue")
            self.continue_button.disabled = False
            self.right_view.update()

        # check if there are additional requirements given in the config
        if self.state.config.requirements:
            # android version
            required_android_version = self.state.config.requirements.get("android")
            if required_android_version:
                android_checkbox = Checkbox(
                    label="The required android version is installed. (Or I know the risk of continuing)",
                    on_change=enable_continue_button,
                )
                android_version_check = Card(
                    Container(
                        content=Column(
                            [
                                Markdown(
                                    f"""
#### Android Version {required_android_version}:
Before following these instructions please ensure that the device is currently using Android {required_android_version} firmware.
If the vendor provided multiple updates for that version, e.g. security updates, make sure you are on the latest!
If your current installation is newer or older than Android {required_android_version}, please upgrade or downgrade to the required
version before proceeding (guides can be found on the internet!).
                    """
                                ),
                                android_checkbox,
                            ]
                        ),
                        padding=10,
                    )
                )
                self.checkboxes.append(android_checkbox)
                self.right_view.controls.append(android_version_check)

            # firmware version
            required_firmware_version = self.state.config.requirements.get("firmware")
            if required_firmware_version:
                firmware_checkbox = Checkbox(
                    label="The required firmware version is installed. (Or I know the risk of continuing)",
                    on_change=enable_continue_button,
                )
                firmware_version_check = Card(
                    Container(
                        content=Column(
                            [
                                Markdown(
                                    f"""
#### Firmware Version {required_firmware_version}:
Before following these instructions please ensure that the device is on firmware version {required_firmware_version}.
To discern this, you can run the command `adb shell getprop ro.build.display.id` on the stock ROM.
If the device is not on the specified version, please follow the instructions below to install it.
                    """
                                ),
                                firmware_checkbox,
                            ]
                        ),
                        padding=10,
                    )
                )
                self.checkboxes.append(firmware_checkbox)
                self.right_view.controls.append(firmware_version_check)

        # default requirements: battery level
        battery_checkbox = Checkbox(
            label="The battery level is over 80%.",
            on_change=enable_continue_button,
        )
        battery_version_check = Card(
            Container(
                content=Column(
                    [
                        Markdown(
                            """
#### Battery level over 80%
Before continuing make sure your device battery level is above 80%.
            """
                        ),
                        battery_checkbox,
                    ]
                ),
                padding=10,
            ),
        )
        self.checkboxes.append(battery_checkbox)
        self.right_view.controls.append(battery_version_check)

        # default requirement: disable lock code and fingerprint
        lock_checkbox = Checkbox(
            label="No lock code or fingerprint lock enabled.",
            on_change=enable_continue_button,
        )
        lock_check = Card(
            Container(
                content=Column(
                    [
                        Markdown(
                            """
#### Disable all device lock codes and fingerprint locks.
            """
                        ),
                        lock_checkbox,
                    ]
                ),
                padding=10,
            ),
        )
        self.checkboxes.append(lock_checkbox)
        self.right_view.controls.append(lock_check)

        # add the final confirm and continue button
        self.right_view.controls.append(Row([self.continue_button], alignment="center"))
        return self.view