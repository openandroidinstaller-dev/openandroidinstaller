"""Contains the install view."""

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
from time import sleep
from typing import Callable

from flet import (
    Column,
    ElevatedButton,
    Row,
    icons,
    Switch,
    colors,
)

from styles import (
    Text,
    Markdown,
)

from views import BaseView
from app_state import AppState
from tooling import adb_twrp_wipe_and_install
from widgets import (
    confirm_button,
    get_title,
    TerminalBox,
    ProgressIndicator,
)


class InstallView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state)
        self.on_confirm = on_confirm

    def build(self):
        """Create the content of the view."""
        # error text
        self.error_text = Text("", color=colors.RED)

        # switch to enable advanced output - here it means show terminal input/output in tool
        def check_advanced_switch(e):
            """Check the box to enable advanced output."""
            if self.advanced_switch.value:
                logger.info("Enable advanced output.")
                self.state.advanced = True
                self.terminal_box.toggle_visibility()
            else:
                logger.info("Disable advanced output.")
                self.state.advanced = False
                self.terminal_box.toggle_visibility()
            self.right_view.update()

        self.advanced_switch = Switch(
            label="Advanced output",
            on_change=check_advanced_switch,
            disabled=False,
        )
        # switch for installing addons
        def check_addons_switch(e):
            """Check the switch to enable the addons installation process."""
            if self.install_addons_switch.value:
                logger.info("Enable flashing addons.")
                # add the addons step here.
                self.state.add_default_views(self.state.addon_views)
                self.state.install_addons = True
            else:
                logger.info("Disable flashing addons.")
                self.state.default_views = []
                self.state.install_addons = False

        self.install_addons_switch = Switch(
            label="Install addons",
            on_change=check_addons_switch,
            disabled=False,
        )
        # text box for terminal output
        self.terminal_box = TerminalBox(expand=True)

        # container for progress indicators
        self.progress_indicator = ProgressIndicator(expand=True)

        # main controls
        self.right_view_header.controls = [
            get_title(
                "Install OS",
                step_indicator_img="steps-header-install.png",
            )
        ]
        self.right_view.controls = [
            Markdown(
                """In the next steps, you finally flash the selected OS image.
            
Connect your device with your computer with the USB-Cable. This step will format your phone and wipe all the data.
It will also remove encryption and delete all files stored in the internal storage.
Then the OS image will be installed. Confirm to install.

This might take a while. At the end your phone will boot into the new OS.
    
#### **Install addons:**
If you want to install any addons like Google Apps, microG or F-droid, use the toggle below **before** starting the install process!
After the installation you'll be taken through the process. Note, that this process is still somewhat experimental and using ROMs with
included Google Apps (like PixelExperience) or microG (lineageOS for microG) is recommended.

#### **Warning:**
Don't try to add addons like Google Apps if your OS ROM already has Google Apps or microG included! Otherwise your system will break!
"""
            )
        ]
        # basic view
        logger.info("Starting installation.")
        self.confirm_button = confirm_button(self.on_confirm)
        self.confirm_button.disabled = True
        # button to run the installation process
        self.install_button = ElevatedButton(
            "Confirm and install",
            on_click=self.run_install,
            expand=True,
            icon=icons.DIRECTIONS_RUN_OUTLINED,
        )
        # build the view
        self.right_view.controls.extend(
            [
                Row([self.error_text]),
                Row([self.progress_indicator]),
                Column(
                    [
                        self.install_addons_switch,
                        self.advanced_switch,
                        Row([self.install_button, self.confirm_button]),
                    ]
                ),
                Row([self.terminal_box]),
            ]
        )

        # if skipping is allowed add a button to the view
        if self.state.test:
            self.right_view.controls.append(
                Row(
                    [
                        Text("Do you want to skip?"),
                        ElevatedButton(
                            "Skip",
                            on_click=self.on_confirm,
                            icon=icons.NEXT_PLAN_OUTLINED,
                            expand=True,
                        ),
                    ]
                )
            )
        return self.view

    def run_install(self, e):
        """
        Run the installation process through twrp.

        Some parts of the command are changed by placeholders.
        """
        # disable the call button while the command is running
        self.install_button.disabled = True
        self.install_addons_switch.disabled = True
        self.error_text.value = ""
        # reset the progress indicators
        self.progress_indicator.clear()
        # reset terminal output
        if self.state.advanced:
            self.terminal_box.clear()
        self.right_view.update()

        # run the install script
        for line in adb_twrp_wipe_and_install(
            target=self.state.image_path,
            config_path=self.state.config_path,
            bin_path=self.state.bin_path,
            install_addons=self.state.install_addons,
            is_ab=self.state.config.is_ab,
            recovery=self.state.recovery_path,
        ):
            # write the line to advanced output terminal
            self.terminal_box.write_line(line)
            # in case the install command is run, we want to update the progress bar
            self.progress_indicator.display_progress_bar(line)
            self.progress_indicator.update()
        success = line  # the last element of the iterable is a boolean encoding success/failure

        # update the view accordingly
        if not success:
            # enable call button to retry
            self.install_button.disabled = False
            # also remove the last error text if it happened
            self.error_text.value = "Installation failed! Try again or make sure everything is setup correctly."
        else:
            sleep(5)  # wait to make sure everything is fine
            logger.success("Installation process was successful. Allow to continue.")
            # enable the confirm button and disable the call button
            self.confirm_button.disabled = False
            self.install_button.disabled = True
        self.view.update()
