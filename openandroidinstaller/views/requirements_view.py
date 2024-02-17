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
from typing import Callable

from app_state import AppState
from flet import (
    AlertDialog,
    Card,
    Checkbox,
    Column,
    Container,
    Divider,
    ElevatedButton,
    OutlinedButton,
    Row,
    TextButton,
    colors,
    icons,
)
from flet_core.buttons import CountinuosRectangleBorder
from loguru import logger
from styles import Markdown, Text
from views import BaseView
from widgets import get_title


class RequirementsView(BaseView):
    """View to display requirements and ask for confirmation."""

    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
        on_back: Callable,
    ):
        super().__init__(state=state, image="requirements-default.png")
        self.on_confirm = on_confirm
        self.on_back = on_back

        self.init_visuals()

    def init_visuals(
        self,
    ):
        """Initialize the stateful visual elements of the view."""
        # checkboxes list
        self.checkboxes = []
        self.checkbox_cards = []
        # continue button
        self.continue_button = ElevatedButton(
            "Continue",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )
        # back button
        self.back_button = ElevatedButton(
            "Back",
            on_click=self.on_back,
            icon=icons.ARROW_BACK,
            expand=True,
        )

        # dialog to explain howto find the android and firmware version
        self.dlg_howto_find_versions = AlertDialog(
            modal=True,
            title=Text("Where to find the current Android and/or firmware version?"),
            content=Markdown(
                """
## Find your current Android Version
Scroll down on the Settings screen and look for an "About phone", "About tablet", or "System" option.
You'll usually find this at the very bottom of the main Settings screen, under System, but depending
on your phone it could be different. If you do find a specific option for System, you can usually
find the "About Phone" underneath that.

On the resulting screen, look for "Android version" to find the version of Android installed on your device.

## Find your current device firmware version
On the same screen you find the "Android version" you can also find the Firmware Version.
On some devices, the build version is basically the firmware version.""",
            ),
            actions=[
                TextButton("Close", on_click=self.close_find_version_dlg),
            ],
            actions_alignment="end",
            shape=CountinuosRectangleBorder(radius=0),
        )

    def build(self):
        self.clear()

        # create help/info button to show the help dialog
        info_button = OutlinedButton(
            "How to Find the version",
            on_click=self.open_find_version_dlg,
            expand=False,
            icon=icons.HELP_OUTLINE_OUTLINED,
            icon_color=colors.DEEP_ORANGE_500,
            tooltip="How to find the firmware and android version of your device.",
        )

        # build up the main view
        self.right_view_header.controls = [
            get_title(
                "Check the Requirements",
                step_indicator_img="steps-header-requirements.png",
            ),
        ]
        self.right_view.controls.extend(
            [
                Text(
                    "Before continuing you need to check some requirements to progress. Please read the instructions and check the boxes if everything is fine."
                ),
                Divider(),
            ]
        )

        if not self.checkboxes:
            # check if there are additional requirements given in the config
            if self.state.config.requirements:
                # android version
                required_android_version = self.state.config.requirements.get("android")
                if required_android_version:
                    android_checkbox = Checkbox(
                        label="The required android version is installed.\n(Or I know the risk of continuing)",
                        on_change=self.enable_continue_button,
                    )
                    android_version_check = Card(
                        Container(
                            content=Column(
                                [
                                    Row(
                                        [
                                            Text(
                                                f"Android Version {required_android_version}:",
                                                style="titleSmall",
                                            ),
                                            info_button,
                                        ],
                                        alignment="spaceBetween",
                                    ),
                                    Markdown(
                                        f"""Before following these instructions please ensure that the device is currently using Android {required_android_version} firmware.
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
                    self.checkbox_cards.append(android_version_check)

                # firmware version
                required_firmware_version = self.state.config.requirements.get(
                    "firmware"
                )
                if required_firmware_version:
                    firmware_checkbox = Checkbox(
                        label="The required firmware version is installed. (Or I know the risk of continuing)",
                        on_change=self.enable_continue_button,
                    )
                    firmware_version_check = Card(
                        Container(
                            content=Column(
                                [
                                    Row(
                                        [
                                            Text(
                                                f"Firmware Version {required_firmware_version}:",
                                                style="titleSmall",
                                            ),
                                            info_button,
                                        ],
                                        alignment="spaceBetween",
                                    ),
                                    Markdown(
                                        f"""Before following these instructions please ensure that the device is on firmware version {required_firmware_version}.
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
                    self.checkbox_cards.append(firmware_version_check)

            battery_checkbox, battery_check_card = self.get_battery_check()
            self.checkboxes.append(battery_checkbox)
            self.checkbox_cards.append(battery_check_card)

            boot_stock_checkbox, boot_stock_check_card = self.get_boot_stock_check()
            self.checkboxes.append(boot_stock_checkbox)
            self.checkbox_cards.append(boot_stock_check_card)

            lock_checkbox, lock_check_card = self.get_lock_check()
            self.checkboxes.append(lock_checkbox)
            self.checkbox_cards.append(lock_check_card)

        # add the checkbox cards
        self.right_view.controls.extend(self.checkbox_cards)

        # add the final confirm and continue button
        self.right_view.controls.append(
            Row([self.back_button, self.continue_button], alignment="center")
        )
        return self.view

    def get_battery_check(self):
        """Get checkbox and card for default requirements: battery level."""
        battery_checkbox = Checkbox(
            label="The battery level is over 80%.",
            on_change=self.enable_continue_button,
        )
        battery_check_card = Card(
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
        return battery_checkbox, battery_check_card

    def get_boot_stock_check(self):
        """Get checkbox and card for default requirements: boot stock once."""
        boot_stock_checkbox = Checkbox(
            label="Booted the stock OS at least once.",
            on_change=self.enable_continue_button,
        )
        boot_stock_check_card = Card(
            Container(
                content=Column(
                    [
                        Markdown(
                            """
#### Boot your device with the stock OS at least once and check every functionality.
Make sure that you can send and receive SMS and place and receive calls (also via WiFi and LTE, if available),
otherwise it won\'t work on your custom ROM either! Additionally, some devices require that VoLTE/VoWiFi be utilized once on stock to provision IMS.
            """
                        ),
                        boot_stock_checkbox,
                    ]
                ),
                padding=10,
            ),
        )
        return boot_stock_checkbox, boot_stock_check_card

    def get_lock_check(self):
        """Get the checkbox and card for the default requirement: disable lock code and fingerprint."""
        lock_checkbox = Checkbox(
            label="No lock code or fingerprint lock enabled.",
            on_change=self.enable_continue_button,
        )
        lock_check_card = Card(
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
        return lock_checkbox, lock_check_card

    def enable_continue_button(self, e):
        """Enable the continue button if all checkboxes are ticked."""
        for checkbox in self.checkboxes:
            if not checkbox.value:
                self.continue_button.disabled = True
                return
        logger.info("All requirements ticked. Allow to continue")
        self.continue_button.disabled = False
        self.right_view.update()

    def open_find_version_dlg(self, e):
        """Open the dialog to explain how to find the android and firmware version."""
        self.page.dialog = self.dlg_howto_find_versions
        self.dlg_howto_find_versions.open = True
        self.page.update()

    def close_find_version_dlg(self, e):
        """Close the dialog to explain how to find the android and firmware version."""
        self.dlg_howto_find_versions.open = False
        self.page.update()
