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
from pathlib import Path

from flet import (
    Column,
    ElevatedButton,
    Row,
    Text,
    icons,
    TextField,
    Container,
    Switch,
    alignment,
    colors,
    ProgressBar,
)

from views import BaseView
from installer_config import Step
from app_state import AppState
from tooling import (
    adb_reboot,
    adb_reboot_bootloader,
    adb_reboot_download,
    adb_sideload,
    adb_twrp_wipe_and_install,
    fastboot_flash_recovery,
    fastboot_oem_unlock,
    fastboot_reboot,
    fastboot_unlock,
    fastboot_unlock_with_code,
    heimdall_flash_recovery,
)
from widgets import call_button, confirm_button, get_title, link_button


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
                self.terminal_box.visible = True
                # add terminal box if enabled
                self.right_view.update()
            else:
                logger.info("Disable advanced output.")
                self.state.advanced = False
                self.terminal_box.visible = False
                self.right_view.update()

        self.advanced_switch = Switch(
            label="Advanced output",
            on_change=check_advanced_switch,
            disabled=False,
        )
        # text box for terminal output
        self.terminal_box = Container(
            content=Column(scroll="auto", expand=True),
            margin=10,
            padding=10,
            alignment=alignment.top_left,
            bgcolor=colors.BLACK38,
            height=300,
            border_radius=2,
            expand=True,
            visible=False
        )
        # main controls
        self.right_view.controls = [
            get_title(f"{self.step.title}"),
            self.state.progressbar,
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
            self.right_view.controls.extend([
                Row([self.error_text]),
                Column(
                    [
                        self.advanced_switch,
                        Row([self.call_button, self.confirm_button]),
                    ]
                ),
                Row([self.terminal_box])
            ])
        elif self.step.type == "call_button_with_input":
            self.confirm_button.disabled = True
            self.call_button = call_button(
                self.call_to_phone, command=self.step.command
            )
            self.right_view.controls.extend(
                [
                    self.inputtext,
                    Row([self.error_text]),
                    Column(
                        [
                            self.advanced_switch,
                            Row([self.call_button, self.confirm_button]),
                        ]
                    ),
                    Row([self.terminal_box])
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
        # disable the call button while the command is running
        self.call_button.disabled = True
        # reset terminal output
        if self.state.advanced:
            self.terminal_box.content.controls = []
        # display a progress bar to show something is happening
        progress_bar = Row(
            [ProgressBar(width=600, color="#00d886", bgcolor="#eeeeee", bar_height=16)],
            alignment="center",
        )
        self.right_view.controls.append(progress_bar)
        self.right_view.update()

        cmd_mapping = {
            "adb_reboot": adb_reboot,
            "adb_reboot_bootloader": adb_reboot_bootloader,
            "adb_reboot_download": adb_reboot_download,
            "fastboot_unlock": fastboot_unlock,
            "fastboot_oem_unlock": fastboot_oem_unlock,
            "fastboot_reboot": fastboot_reboot,
        }

        # run the right command
        if command in cmd_mapping.keys():
            for line in cmd_mapping.get(command)(bin_path=self.state.bin_path):
                if (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "adb_sideload":
            for line in adb_sideload(
                bin_path=self.state.bin_path, target=self.state.image_path
            ):
                if (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "adb_twrp_wipe_and_install":
            for line in adb_twrp_wipe_and_install(
                bin_path=self.state.bin_path,
                target=self.state.image_path,
                config_path=self.state.config_path.joinpath(
                    Path(f"{self.state.config.metadata.get('devicecode')}.yaml")
                ),
            ):
                if (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "fastboot_flash_recovery":
            for line in fastboot_flash_recovery(
                bin_path=self.state.bin_path, recovery=self.state.recovery_path
            ):
                if (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "fastboot_unlock_with_code":
            for line in fastboot_unlock_with_code(
                bin_path=self.state.bin_path, unlock_code=self.inputtext.value
            ):
                if (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "heimdall_flash_recovery":
            for line in heimdall_flash_recovery(
                bin_path=self.state.bin_path, recovery=self.state.recovery_path
            ):
                if (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        else:
            msg = f"Unknown command type: {command}. Stopping."
            logger.error(msg)
            self.error_text.value = msg
            raise Exception(msg)

        # update the view accordingly
        if not success:
            # enable call button to retry
            self.call_button.disabled = False
            # pop the progress bar
            self.right_view.controls.remove(progress_bar)
            # also remove the last error text if it happened
            self.error_text.value = f"Command {command} failed! Try again or make sure everything is setup correctly."
        else:
            sleep(5)  # wait to make sure everything is fine
            logger.success(f"Command {command} run successfully. Allow to continue.")
            # pop the progress bar
            self.right_view.controls.remove(progress_bar)
            # emable the confirm buton and disable the call button
            self.confirm_button.disabled = False
            self.call_button.disabled = True
        self.view.update()
