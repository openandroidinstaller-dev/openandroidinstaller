"""Contains the steps view."""

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
from functools import partial

from flet import (
    Column,
    ElevatedButton,
    Row,
    icons,
    TextField,
    Switch,
    colors,
)


from styles import (
    Text,
)

from views import BaseView
from installer_config import Step
from app_state import AppState
from tooling import (
    adb_reboot,
    adb_reboot_bootloader,
    adb_reboot_download,
    adb_sideload,
    adb_twrp_copy_partitions,
    fastboot_boot_recovery,
    fastboot_flash_boot,
    fastboot_oem_unlock,
    fastboot_reboot,
    fastboot_unlock,
    fastboot_unlock_with_code,
    fastboot_get_unlock_data,
    heimdall_flash_recovery,
)
from widgets import (
    call_button,
    confirm_button,
    get_title,
    link_button,
    TerminalBox,
    ProgressIndicator,
)


class StepView(BaseView):
    def __init__(
        self,
        step: Step,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state, image=step.img)
        self.step = step
        self.on_confirm = on_confirm

        # text input
        self.inputtext = TextField(
            hint_text="your unlock code", expand=False
        )  # textfield for the unlock code

    def build(self):
        """Create the content of a view from step."""
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
            value=self.state.advanced,
        )
        # text box for terminal output
        self.terminal_box = TerminalBox(expand=True, visible=self.state.advanced)

        # container for progress indicators
        self.progress_indicator = ProgressIndicator(expand=True)

        # main controls
        steps_indictor_img_lookup = {
            "Unlock the bootloader": "steps-header-unlock.png",
            "Boot custom recovery": "steps-header-recovery.png",
        }
        self.right_view_header.controls = [
            get_title(
                f"{self.step.title}",
                step_indicator_img=steps_indictor_img_lookup.get(self.step.title),
            )
        ]
        self.right_view.controls = [
            Text(f"{self.step.content}"),
        ]
        # basic view depending on step.type
        logger.info(f"Starting step of type {self.step.type}.")
        self.confirm_button = confirm_button(self.on_confirm)
        if self.step.type == "confirm_button":
            self.right_view.controls.append(Row([self.confirm_button]))
        elif self.step.type == "call_button":
            self.confirm_button.disabled = True
            self.call_button = call_button(
                self.call_to_phone, command=self.step.command
            )
            self.right_view.controls.extend(
                [
                    Row([self.error_text]),
                    Row([self.progress_indicator]),
                    Column(
                        [
                            self.advanced_switch,
                            Row([self.call_button, self.confirm_button]),
                        ]
                    ),
                    Row([self.terminal_box]),
                ]
            )
        elif self.step.type == "call_button_with_input":
            self.confirm_button.disabled = True
            self.call_button = call_button(
                self.call_to_phone, command=self.step.command
            )
            self.right_view.controls.extend(
                [
                    self.inputtext,
                    Row([self.error_text]),
                    Row([self.progress_indicator]),
                    Column(
                        [
                            self.advanced_switch,
                            Row([self.call_button, self.confirm_button]),
                        ]
                    ),
                    Row([self.terminal_box]),
                ]
            )
        elif self.step.type == "link_button_with_confirm":
            self.right_view.controls.extend(
                [Row([link_button(self.step.link, "Open Link"), self.confirm_button])]
            )

        elif self.step.type != "text":
            logger.error(f"Unknown step type: {self.step.type}")
            raise Exception(f"Unknown step type: {self.step.type}")

        # if skipping is allowed add a button to the view
        if self.step.allow_skip or self.state.test:
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

    def call_to_phone(self, e, command: str):
        """
        Run the command given on the phone.

        Some parts of the command are changed by placeholders.
        """
        # clean the previous error display
        self.error_text.value = ""
        # disable the call button while the command is running
        self.call_button.disabled = True
        # reset the progress indicators
        self.progress_indicator.clear()
        # reset terminal output
        if self.state.advanced:
            self.terminal_box.clear()
        self.right_view.update()

        # get the appropriate function to run for every possible command.
        cmd_mapping = {
            "adb_reboot": adb_reboot,
            "adb_reboot_bootloader": adb_reboot_bootloader,
            "adb_reboot_download": adb_reboot_download,
            "adb_sideload": partial(adb_sideload, target=self.state.image_path),
            "adb_twrp_copy_partitions": partial(
                adb_twrp_copy_partitions, config_path=self.state.config_path
            ),
            "fastboot_unlock": fastboot_unlock,
            "fastboot_unlock_with_code": partial(
                fastboot_unlock_with_code, unlock_code=self.inputtext.value
            ),
            "fastboot_oem_unlock": fastboot_oem_unlock,
            "fastboot_get_unlock_data": fastboot_get_unlock_data,
            "fastboot_boot_recovery": partial(
                fastboot_boot_recovery,
                recovery=self.state.recovery_path,
                is_ab=self.state.config.is_ab,
            ),
            "fastboot_flash_boot": partial(
                fastboot_flash_boot,
                recovery=self.state.recovery_path,
            ),
            "fastboot_reboot": fastboot_reboot,
            "heimdall_flash_recovery": partial(
                heimdall_flash_recovery, recovery=self.state.recovery_path
            ),
        }

        # run the right command
        if command in cmd_mapping.keys():
            for line in cmd_mapping.get(command)(bin_path=self.state.bin_path):  # type: ignore
                # write the line to advanced output terminal
                self.terminal_box.write_line(line)
                self.progress_indicator.display_progress_ring()
        else:
            msg = f"Unknown command type: {command}. Stopping."
            logger.error(msg)
            self.error_text.value = msg
            raise Exception(msg)
        success = line  # the last element of the iterable is a boolean encoding success/failure

        # update the view accordingly
        if not success:
            # enable call button to retry
            self.call_button.disabled = False
            # also remove the last error text if it happened
            self.error_text.value = f"Command {command} failed! Try again or make sure everything is setup correctly."
        else:
            sleep(5)  # wait to make sure everything is fine
            logger.success(f"Command {command} run successfully. Allow to continue.")
            # enable the confirm button and disable the call button
            self.confirm_button.disabled = False
            self.call_button.disabled = True
        # reset the progress indicator (let the progressbar stay for the install command)
        self.progress_indicator.clear()
        self.view.update()
