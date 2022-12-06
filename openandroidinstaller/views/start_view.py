"""Contains the start view."""

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
    AlertDialog,
    Switch,
    Column,
    Divider,
    ElevatedButton,
    FilledButton,
    Markdown,
    Row,
    Text,
    TextButton,
    colors,
    icons,
)
from flet.buttons import CountinuosRectangleBorder

from views import BaseView
from app_state import AppState
from widgets import get_title
from tooling import search_device


class StartView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state, image="connect-to-usb.png")
        self.on_confirm = on_confirm

    def build(self):
        self.continue_button = ElevatedButton(
            "Continue",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )

        # dialog box to help with developer options
        self.dlg_help_developer_options = AlertDialog(
            modal=True,
            title=Text("How to enable developer options and OEM unlocking"),
            content=Markdown(
                """
To do this, tap seven times on the build number in the 'System'- or 'About the phone'-Menu in Settings. You can also use the phones own search to look for `build number`. 
Then go back to the main menu and look for 'developer options'. You can also search for it in your phone.
When you are in developer options, toggle OEM unlocking and USB-Debugging. If your phone is already connected to your PC, a pop-up might appear. Allow USB debugging in the pop-up on your phone.
Now you are ready to continue.
"""
            ),
            actions=[
                TextButton("Close", on_click=self.close_developer_options_dlg),
            ],
            actions_alignment="end",
            shape=CountinuosRectangleBorder(radius=0),
        )
        # toggleswitch to allow skipping unlocking the bootloader
        def check_bootloader_unlocked(e):
            """Enable skipping unlocking the bootloader if selected."""
            if self.bootloader_switch.value:
                logger.info("Skipping bootloader unlocking.")
                self.state.steps = (
                    self.state.config.flash_recovery + self.state.config.install_os
                )
                self.state.num_total_steps = len(self.state.steps)
            else:
                logger.info("Enabled unlocking the bootloader again.")
                self.state.steps = (
                    self.state.config.unlock_bootloader
                    + self.state.config.flash_recovery
                    + self.state.config.install_os
                )
                self.state.num_total_steps = len(self.state.steps)

        self.bootloader_switch = Switch(
            label="Bootloader is already unlocked.",
            on_change=check_bootloader_unlocked,
            disabled=True,
        )

        # inform the user about the device detection
        self.device_name = Text("", weight="bold")
        self.device_detection_infobox = Row(
            [Text("Detected device:"), self.device_name]
        )

        # build up the main view
        self.right_view.controls.extend(
            [
                get_title("Welcome to the OpenAndroidInstaller!"),
                Text(
                    "We will walk you through the installation process nice and easy."
                ),
                Divider(),
                Markdown(
                    """
Before you continue, make sure
- your devices is on the latest system update.
- you have a backup of all your important data, since this procedure will **erase all data from the phone**.
- to not store the backup on the phone! 

Please note, that vendor specific back-ups will most likely not work on LineageOS!
                """
                ),
                Divider(),
                Markdown(
                    """
To get started you need to 
- **enable developer options** on your device
- and then **enable USB debugging** and **OEM unlocking** in the developer options.
                """
                ),
                Row(
                    [
                        ElevatedButton(
                            "How do I enable developer options?",
                            on_click=self.open_developer_options_dlg,
                            expand=True,
                            tooltip="Get help to enable developer options and OEM unlocking.",
                        )
                    ]
                ),
                Divider(),
                Markdown(
                    """
Now 
- **connect your device to this computer via USB** and
- **allow USB debugging in the pop-up on your phone**.
- Then **press the button 'Search device'**.
When everything works correctly you should see your device name here and you can continue.
                """
                ),
                Divider(),
                Column(
                    [
                        self.device_detection_infobox,
                        Row([self.bootloader_switch]),
                    ]
                ),
                Row(
                    [
                        FilledButton(
                            "Search for device",
                            on_click=self.search_devices,
                            icon=icons.PHONE_ANDROID,
                            expand=True,
                            tooltip="Search for a connected device.",
                        ),
                        self.continue_button,
                    ],
                    alignment="center",
                ),
            ]
        )
        return self.view

    def open_developer_options_dlg(self, e):
        """Open the dialog for help to developer mode."""
        self.page.dialog = self.dlg_help_developer_options
        self.dlg_help_developer_options.open = True
        self.page.update()

    def close_developer_options_dlg(self, e):
        """Close the dialog for help to developer mode."""
        self.dlg_help_developer_options.open = False
        self.page.update()

    def search_devices(self, e):
        """Search the device when the button is clicked."""
        # search the device
        if self.state.test:
            # this only happens for testing
            device_code = self.state.test_config
            logger.info(
                f"Running search in development mode and loading config {device_code}.yaml."
            )
        else:
            device_code = search_device(
                platform=self.state.platform, bin_path=self.state.bin_path
            )
            if device_code:
                self.device_name.value = device_code
                self.device_name.color = colors.BLACK
            else:
                logger.info("No device detected! Connect to USB and try again.")
                self.device_name.value = (
                    "No device detected! Connect to USB and try again."
                )
                self.device_name.color = colors.RED

        # load the config, if a device is detected
        if device_code:
            self.device_name.value = device_code
            # load config from file
            self.state.load_config(device_code)
            if self.state.config:
                device_name = self.state.config.metadata.get(
                    "devicename", "No device name in config."
                )
            else:
                device_name = None

            # display success in the application
            if device_name:
                self.continue_button.disabled = False
                self.bootloader_switch.disabled = False
                # overwrite the text field with the real name from the config
                self.device_name.value = f"{device_name} (code: {device_code})"
                self.device_name.color = colors.GREEN
            else:
                # failed to load config
                logger.error(f"Failed to load config for {device_code}.")
                self.device_name.value = (
                    f"Failed to load config for device with code {device_code}."
                )
                self.device_name.color = colors.RED
        self.view.update()
