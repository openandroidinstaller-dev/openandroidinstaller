"""Contains the install addons view."""

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
from pathlib import Path

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
from tooling import adb_twrp_install_addon, adb_twrp_finish_install_addons, adb_reboot
from widgets import (
    confirm_button,
    get_title,
    TerminalBox,
    ProgressIndicator,
)


class InstallAddonsView(BaseView):
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
        # text field to inform about the currently installing addon
        self.addon_info_text = Text("", weight="bold")

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

        # text box for terminal output
        self.terminal_box = TerminalBox(expand=True)

        # container for progress indicators
        self.progress_indicator = ProgressIndicator(expand=True)

        # main controls
        self.right_view_header.controls = [
            get_title(
                "Install Addons",
                step_indicator_img="steps-header-install.png",
            )
        ]
        self.right_view.controls = [
            Markdown(
                """In the next steps, you flash the selected Addons.

Confirm to install.

This might take a while. At the end your phone will boot into the new OS.
"""
            )
        ]
        # basic view
        logger.info("Starting addon installation.")
        self.confirm_button = confirm_button(self.on_confirm)
        self.confirm_button.disabled = True
        # button to run the installation process
        self.install_button = ElevatedButton(
            "Confirm and install addons",
            on_click=self.run_install_addons,
            expand=True,
            icon=icons.DIRECTIONS_RUN_OUTLINED,
        )
        # build the view
        self.right_view.controls.extend(
            [
                Row([self.addon_info_text]),
                Row([self.progress_indicator]),
                Row([self.error_text]),
                Column(
                    [
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

    def run_install_addons(self, e):
        """
        Run the addon installation process through twrp.

        Some parts of the command are changed by placeholders.
        """
        # disable the call button while the command is running
        self.install_button.disabled = True
        self.error_text.value = ""
        self.addon_info_text.value = ""
        # reset terminal output
        if self.state.advanced:
            self.terminal_box.clear()
        self.right_view.update()

        # run the install script
        for addon_num, addon_path in enumerate(self.state.addon_paths):
            # reset the progress indicators
            self.progress_indicator.clear()
            # inform about the currently installed addon
            self.addon_info_text.value = f"{addon_num + 1}/{len(self.state.addon_paths)}: Installing {Path(addon_path).name} ..."
            self.right_view.update()

            # install one addon at the time
            for line in adb_twrp_install_addon(
                addon_path=addon_path,
                bin_path=self.state.bin_path,
                is_ab=self.state.config.is_ab,
            ):
                # write the line to advanced output terminal
                self.terminal_box.write_line(line)
                # in case the install command is run, we want to update the progress bar
                self.progress_indicator.display_progress_bar(line)
                self.progress_indicator.update()
            sleep(7)

        if self.state.addon_paths:
            # reboot after installing the addons; here we might switch partitions on ab-partitioned devices
            for line in adb_twrp_finish_install_addons(
                bin_path=self.state.bin_path,
                is_ab=self.state.config.is_ab,
            ):
                self.terminal_box.write_line(line)
        else:
            logger.info("No addons selected. Rebooting to OS.")
            for line in adb_reboot(bin_path=self.state.bin_path):
                # write the line to advanced output terminal
                self.terminal_box.write_line(line)
        success = line  # the last element of the iterable is a boolean encoding success/failure

        # update the view accordingly
        if not success:
            # enable call button to retry
            self.install_button.disabled = False
            # also remove the last error text if it happened
            self.error_text.value = "Installation failed! Try again or make sure everything is setup correctly."
        else:
            sleep(4)  # wait to make sure everything is fine
            self.progress_indicator.set_progress_bar(100)
            self.progress_indicator.update()
            logger.success("Installation process was successful. Allow to continue.")
            # enable the confirm button and disable the call button
            self.confirm_button.disabled = False
            self.install_button.disabled = True
        self.view.update()
