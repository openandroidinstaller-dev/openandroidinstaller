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

import copy
import webbrowser
from loguru import logger
from typing import Callable

from flet import (
    AlertDialog,
    Switch,
    Column,
    Divider,
    ElevatedButton,
    OutlinedButton,
    FilledButton,
    Row,
    TextButton,
    colors,
    icons,
)
from flet_core.buttons import CountinuosRectangleBorder

from styles import (
    Text,
    Markdown,
)
from views import BaseView
from app_state import AppState
from widgets import get_title
from tooling import search_device


class StartView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
        on_back: Callable,
    ):
        super().__init__(state=state, image="connect-to-usb.png")
        self.on_confirm = on_confirm
        self.on_back = on_back

        self.init_visuals()

    def init_visuals(
        self,
    ):
        """Initialize the stateful visual elements of the view."""
        self.continue_button = ElevatedButton(
            "Continue",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )
        self.back_button = ElevatedButton(
            "Back",
            on_click=self.on_back,
            icon=icons.ARROW_BACK,
            expand=True,
        )

        # dialog box to help with developer options
        self.dlg_help_developer_options = AlertDialog(
            modal=True,
            title=Text("How to enable developer options and OEM unlocking"),
            content=Markdown(
                """
To do this, 
- **tap seven times on the build number** in the 'System'- or 'About the phone'-Menu in Settings. You can also use the phones own search to look for `build number`. 
- Then go back to the main menu and look for **'developer options'**. You can also search for it in your phone.
- When you are in developer options, **toggle OEM unlocking and USB-Debugging**.
- If your phone is already connected to your PC, a pop-up might appear. **Allow USB debugging in the pop-up on your phone.**

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
                self.state.steps = []
            else:
                logger.info("Enabled unlocking the bootloader again.")
                self.state.steps = copy.deepcopy(self.state.config.unlock_bootloader)
            # if the recovery is already flashed, skip flashing it again
            if self.recovery_switch.value == False:
                self.state.steps += copy.deepcopy(self.state.config.boot_recovery)

        self.bootloader_switch = Switch(
            label="Bootloader is already unlocked.",
            on_change=check_bootloader_unlocked,
            disabled=True,
            inactive_thumb_color=colors.YELLOW,
            active_color=colors.GREEN,
        )

        # toggleswitch to allow skipping flashing recovery
        def check_recovery_already_flashed(e):
            """Enable skipping flashing recovery if selected."""

            # manage the bootloader unlocking switch
            if self.bootloader_switch.value == False:
                self.state.steps = copy.deepcopy(self.state.config.unlock_bootloader)
            else:
                self.state.steps = []

            if self.recovery_switch.value:
                logger.info("Skipping flashing recovery.")
            else:
                logger.info("Enabled flashing recovery again.")
                self.state.steps += copy.deepcopy(self.state.config.boot_recovery)

        self.recovery_switch = Switch(
            label="Custom recovery is already flashed.",
            on_change=check_recovery_already_flashed,
            disabled=False,
            inactive_thumb_color=colors.YELLOW,
            active_color=colors.GREEN,
        )

        # inform the user about the device detection
        self.device_name = Text("", weight="bold")
        self.device_detection_infobox = Row(
            [Text("Detected device:"), self.device_name]
        )
        self.device_request_row = Row([], alignment="center")
        self.device_infobox = Column(
            [
                self.device_detection_infobox,
                self.device_request_row,
            ]
        )

    def build(self):
        self.clear()

        # build up the main view
        self.right_view_header.controls.extend(
            [
                get_title(
                    "Get the phone ready",
                    step_indicator_img="steps-header-get-ready.png",
                )
            ]
        )
        self.right_view.controls.extend(
            [
                Markdown(
                    """
To get started you need to 
- **enable developer options** on your device
- and then **enable USB debugging** and **OEM unlocking** in the developer options.
                """
                ),
                Row(
                    [
                        OutlinedButton(
                            "How do I enable developer options?",
                            on_click=self.open_developer_options_dlg,
                            expand=True,
                            icon=icons.HELP_OUTLINE_OUTLINED,
                            icon_color=colors.DEEP_ORANGE_500,
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
- You might also need to **activate "data transfer"** in the connection settings.
- Then **press the button 'Search device'**.

When everything works correctly you should see your device name here and you can continue.
                """
                ),
                Divider(),
                Markdown(
                    """
If you **already unlocked the bootloader** of your device or already **flashed a custom recovery**, please toggle the respective switch below, to skip the procedure.
If you don't know what this means, you most likely don't need to do anything and you can just continue.
            """
                ),
                Row([self.bootloader_switch]),
                Row([self.recovery_switch]),
                Divider(),
                self.device_infobox,
                Row(
                    [
                        self.back_button,
                        FilledButton(
                            "Search for device",
                            on_click=self.search_devices_clicked,
                            icon=icons.DEVICES_OTHER_OUTLINED,
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

    def search_devices_clicked(self, e):
        """Search the device when the button is clicked."""
        self.device_request_row.controls.clear()
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
                    "device_name", "No device name in config."
                )
            else:
                device_name = None

            # display success in the application
            if device_name:
                self.continue_button.disabled = False
                self.bootloader_switch.disabled = False
                # overwrite the text field with the real name from the config
                self.device_name.value = (
                    f"{device_name} (code: {self.state.config.device_code})"
                )
                self.device_name.color = colors.GREEN
                # if there are no steps for bootloader unlocking, assume there is nothing to do and toggle the switch
                if len(self.state.config.unlock_bootloader) == 0:
                    self.bootloader_switch.value = True
            else:
                # failed to load config or device is not supported
                logger.error(
                    f"Device with code '{device_code}' is not supported or the config is corrupted. Please check the logs for more information."
                )
                self.device_name.value = (
                    f"Device with code '{device_code}' is not supported yet."
                )
                # add request support for device button
                request_url = f"https://github.com/openandroidinstaller-dev/openandroidinstaller/issues/new?labels=device&template=device-support-request.yaml&title=Add support for {device_code}"
                self.device_request_row.controls.append(
                    ElevatedButton(
                        "Request support for this device",
                        icon=icons.PHONELINK_SETUP_OUTLINED,
                        on_click=lambda _: webbrowser.open(request_url),
                    )
                )
                self.device_name.color = colors.RED
        self.view.update()
