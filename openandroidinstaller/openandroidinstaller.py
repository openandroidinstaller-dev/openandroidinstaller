"""Main file of the OpenAndroidInstaller."""

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

import sys
import webbrowser
from pathlib import Path
from subprocess import STDOUT, CalledProcessError, call, check_output
from time import sleep
from typing import Callable, Optional

import flet
from flet import (
    AlertDialog,
    AppBar,
    Banner,
    Checkbox,
    Column,
    Container,
    Divider,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilledButton,
    Icon,
    Image,
    Page,
    ProgressBar,
    ProgressRing,
    Row,
    Text,
    TextButton,
    TextField,
    UserControl,
    VerticalDivider,
    colors,
    icons,
)
from installer_config import InstallerConfig, Step
from loguru import logger
from tool_utils import call_tool_with_command, search_device
from widgets import call_button, confirm_button, get_title

# Toggle to True for development purposes
DEVELOPMENT = False
DEVELOPMENT_CONFIG = "sargo"  # "a3y17lte"  # "sargo"


PLATFORM = sys.platform
# Define asset paths
CONFIG_PATH = Path(__file__).parent.joinpath(Path("assets/configs")).resolve()
IMAGE_PATH = Path(__file__).parent.joinpath(Path("assets/imgs")).resolve()
BIN_PATH = Path(__file__).parent.joinpath(Path("bin")).resolve()


class BaseView(UserControl):
    def __init__(self, image: str = "placeholder.png"):
        super().__init__()
        self.right_view = Column(expand=True)
        self.left_view = Column(
            width=480,
            controls=[Image(src=IMAGE_PATH.joinpath(Path(image)))],
            expand=True,
            horizontal_alignment="center",
        )
        # main view row
        self.view = Row(
            [self.left_view, VerticalDivider(), self.right_view],
            alignment="spaceEvenly",
        )


class WelcomeView(BaseView):
    def __init__(self, on_confirm: Callable, load_config: Callable, page: Page):
        super().__init__(image="connect-to-usb.png")
        self.on_confirm = on_confirm
        self.load_config = load_config
        self.page = page

    def build(self):
        self.continue_button = ElevatedButton(
            "Continue",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )
        self.device_name = Text("")
        self.config_found_box = Checkbox(
            label="Device config found:",
            value=False,
            disabled=True,
            label_position="left",
        )
        self.dlg_help_developer_options = AlertDialog(
            modal=True,
            title=Text("How to enable developer options and OEM unlocking"),
            content=Text(
                "To do this, tap seven times on the build number in the 'System'- or 'About the phone'-Menu in Settings. Then in developer options, toggle OEM unlocking and USB-Debugging."
            ),
            actions=[
                TextButton("Close", on_click=self.close_developer_options_dlg),
            ],
            actions_alignment="end",
        )
        self.right_view.controls.extend(
            [
                get_title("Welcome to the OpenAndroidInstaller!"),
                Text(
                    "We will walk you through the installation process nice and easy."
                ),
                Divider(),
                Text(
                    "Before you continue, make sure your devices is on the latest system update. Also make sure you have a backup of all your important data, since this procedure will erase all data from the phone. Please store the backup not on the phone! Note, that vendor specific back-ups might not work on LineageOS!"
                ),
                Divider(),
                Text(
                    "Enable USB debugging and OEM unlocking on your device by enabling developer options."
                ),
                Row(
                    [
                        FilledButton(
                            "How do I enable developer mode?",
                            on_click=self.open_developer_options_dlg,
                            expand=True,
                            tooltip="Get help to enable developer options and OEM unlocking.",
                        )
                    ]
                ),
                Divider(),
                Text(
                    "Now connect your device to this computer via USB and allow USB debugging in the pop-up on your phone. Then press 'Search device'. When everything works correctly you should see your device name here."
                ),
                Divider(),
                Column(
                    [
                        Row([Text("Detected device:"), self.device_name]),
                        self.config_found_box,
                    ]
                ),
                Row(
                    [
                        ElevatedButton(
                            "Search device",
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
        if DEVELOPMENT:
            # this only happens for testing
            device_code = DEVELOPMENT_CONFIG
            logger.info(
                f"Running search in development mode and loading config {device_code}.yaml."
            )
        else:
            device_code = search_device(platform=PLATFORM, bin_path=BIN_PATH)
            if device_code:
                self.device_name.value = device_code
            else:
                self.device_name.value = (
                    "No device detected! Connect to USB and try again."
                )

        # load the config, if a device is detected
        if device_code:
            self.device_name.value = device_code
            # load config from file
            path = CONFIG_PATH.joinpath(Path(f"{device_code}.yaml"))
            device_name = self.load_config(path)

            # display success in the application
            if device_name:
                self.config_found_box.value = True
                self.continue_button.disabled = False
                # overwrite the text field with the real name from the config
                self.device_name.value = f"{device_name} (code: {device_code})"
            else:
                # failed to load config
                logger.info(f"Failed to load config from {path}.")
        self.view.update()


class SelectFilesView(BaseView):
    def __init__(
        self,
        on_confirm: Callable,
        progressbar: ProgressBar,
        pick_image_dialog: Callable,
        pick_recovery_dialog: Callable,
        selected_image: Text,
        selected_recovery: Text,
    ):
        super().__init__()
        self.on_confirm = on_confirm
        self.progressbar = progressbar
        self.pick_image_dialog = pick_image_dialog
        self.pick_recovery_dialog = pick_recovery_dialog
        self.selected_image = selected_image
        self.selected_recovery = selected_recovery

    def build(self):
        self.confirm_button = confirm_button(self.on_confirm)
        self.confirm_button.disabled = True

        self.pick_recovery_dialog.on_result = self.enable_button_if_ready
        self.pick_image_dialog.on_result = self.enable_button_if_ready

        self.right_view.controls.append(self.pick_image_dialog)
        self.right_view.controls.append(self.pick_recovery_dialog)
        self.right_view.controls.extend(
            [
                get_title("Pick image and recovery files:"),
                self.progressbar,
                Row(
                    [
                        ElevatedButton(
                            "Pick image file",
                            icon=icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_image_dialog.pick_files(
                                allow_multiple=False,
                                file_type="custom",
                                allowed_extensions=["zip"],
                            ),
                            expand=True,
                        ),
                    ]
                ),
                self.selected_image,
                Row(
                    [
                        ElevatedButton(
                            "Pick recovery file",
                            icon=icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_recovery_dialog.pick_files(
                                allow_multiple=False,
                                file_type="custom",
                                allowed_extensions=["img"],
                            ),
                            expand=True,
                        ),
                    ]
                ),
                self.selected_recovery,
                Divider(),
                Text("If you selected both files you can continue."),
                Row([self.confirm_button]),
            ]
        )
        return self.view

    def enable_button_if_ready(self, e):
        """Enable the confirm button if both files have been selected."""
        if self.selected_image.value and self.selected_recovery.value:
            self.confirm_button.disabled = False
            self.right_view.update()
        else:
            self.confirm_button.disabled = True


class SuccessView(BaseView):
    def __init__(self, progressbar: ProgressBar):
        super().__init__(image="success.png")
        self.progressbar = progressbar

    def build(
        self,
    ):
        self.right_view.controls = [
            get_title("Installation completed successfully!"),
            self.progressbar,
            Row(
                [
                    ElevatedButton(
                        "Finish and close",
                        expand=True,
                        on_click=lambda _: self.page.window_close(),
                    )
                ]
            ),
        ]
        return self.view


class MainView(UserControl):
    def __init__(self):
        super().__init__()
        self.config = None
        # initialize the progress bar indicator
        self.progress_bar = ProgressBar(
            width=480, color="#00d886", bgcolor="#eeeeee", bar_height=16
        )
        self.progress_bar.value = 0
        # create the main columns
        self.view = Column(expand=True, width=800)
        # initialize global stuff
        # file pickers
        self.pick_image_dialog = FilePicker(on_result=self.pick_image_result)
        self.pick_recovery_dialog = FilePicker(on_result=self.pick_recovery_result)
        self.selected_image = Text()
        self.selected_recovery = Text()

        # text input
        self.inputtext = TextField(
            hint_text="your unlock code", expand=False
        )  # textfield for the unlock code

        # paths
        self.image_path = ""
        self.recovery_path = ""

        # create default starter views
        welcome = WelcomeView(
            on_confirm=self.confirm, load_config=self.load_config, page=self.page
        )
        select_files = SelectFilesView(
            on_confirm=self.confirm,
            progressbar=self.progress_bar,
            pick_image_dialog=self.pick_image_dialog,
            pick_recovery_dialog=self.pick_recovery_dialog,
            selected_image=self.selected_image,
            selected_recovery=self.selected_recovery,
        )
        # ordered to allow for pop
        self.default_views = [select_files, welcome]
        # create the final success view
        self.final_view = SuccessView(progressbar=self.progress_bar)
        # keep track of the number of steps
        self.num_steps = 2

    def build(self):
        self.view.controls.append(self.default_views.pop())
        return self.view

    def confirm(self, e):
        """Confirmation event handler to use in downstream views."""
        # remove all elements from column view
        self.view.controls = []
        # if a config is loaded, display a progress bar
        if self.config:
            self.progress_bar.value = (self.num_steps - 1) / (
                self.num_total_steps + 2
            )  # don't show on the first step
            self.num_steps += 1  # increase the step counter
        # if there are default views left, display them first
        if self.default_views:
            self.view.controls.append(self.default_views.pop())
        elif self.config.steps:
            self.view.controls.append(
                StepView(
                    step=self.config.steps.pop(0),
                    on_confirm=self.confirm,
                    progressbar=self.progress_bar,
                    inputtext=self.inputtext,
                    image_path=self.image_path,
                    recovery_path=self.recovery_path,
                )
            )
        else:
            # display the final view
            self.view.controls.append(self.final_view)
        self.view.update()

    def load_config(self, path: str) -> Optional[str]:
        """Function to load a config file from path."""
        try:
            self.config = InstallerConfig.from_file(path)
            self.num_total_steps = len(self.config.steps)
            logger.info(f"Loaded device config from {path}.")
            logger.info(f"Config metadata: {self.config.metadata}.")
            return self.config.metadata.get("devicename", "No device name in config.")
        except FileNotFoundError:
            logger.info(f"No device config found for {path}.")
            return None

    def pick_image_result(self, e: FilePickerResultEvent):
        self.selected_image.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.image_path = e.files[0].path
        logger.info(f"Selected image from {self.image_path}")
        self.selected_image.update()

    def pick_recovery_result(self, e: FilePickerResultEvent):
        self.selected_recovery.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.recovery_path = e.files[0].path
        logger.info(f"Selected recovery from {self.recovery_path}")
        self.selected_recovery.update()


class StepView(BaseView):
    def __init__(
        self,
        step: Step,
        on_confirm: Callable,
        progressbar: ProgressBar,
        inputtext: TextField,
        image_path: str,
        recovery_path: str,
    ):
        super().__init__(step.img)
        self.step = step
        self.on_confirm = on_confirm
        self.progressbar = progressbar
        self.inputtext = inputtext
        self.image_path = image_path
        self.recovery_path = recovery_path

    def build(self):
        """Create the content of a view from step."""
        self.right_view.controls = [
            get_title(f"{self.step.title}"),
            self.progressbar,
            Text(f"{self.step.content}"),
        ]
        # basic view depending on step.type
        if self.step.type == "confirm_button":
            self.confirm_button = confirm_button(self.on_confirm)
            self.right_view.controls.append(Row([self.confirm_button]))
        elif self.step.type == "call_button":
            self.confirm_button = confirm_button(self.on_confirm)
            self.confirm_button.disabled = True
            self.call_button = call_button(
                self.call_to_phone, command=self.step.command
            )
            self.right_view.controls.append(
                Row([self.call_button, self.confirm_button])
            )
        elif self.step.type == "call_button_with_input":
            self.confirm_button = confirm_button(self.on_confirm)
            self.confirm_button.disabled = True
            self.call_button = call_button(
                self.call_to_phone, command=self.step.command
            )
            self.right_view.controls.extend(
                [self.inputtext, Row([self.call_button, self.confirm_button])]
            )
        elif self.step.type != "text":
            raise Exception(f"Unknown step type: {self.step.type}")

        # if skipping is allowed add a button to the view
        if self.step.allow_skip or DEVELOPMENT:
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
        command = command.replace("<recovery>", self.recovery_path)
        command = command.replace("<image>", self.image_path)
        command = command.replace("<inputtext>", self.inputtext.value)

        self.right_view.controls.append(
            Row(
                [ProgressRing(color="#00d886")],
                alignment="center",
            )
        )
        self.right_view.update()
        # run the command
        success = call_tool_with_command(command=command, bin_path=BIN_PATH)
        # update the view accordingly
        if success:
            # pop the progress ring
            self.right_view.controls.pop()
            self.right_view.controls.append(
                Text(
                    f"Command {command} failed! Try again or make sure everything is setup correctly."
                )
            )
        else:
            sleep(5)  # wait to make sure everything is fine
            # pop the progress ring
            self.right_view.controls.pop()
            self.confirm_button.disabled = False
            self.call_button.disabled = True
        self.view.update()


def main(page: Page):
    logger.info(f"Running OpenAndroidInstaller on {PLATFORM}")
    # Configure the application base page
    page.title = "OpenAndroidInstaller"
    page.window_height = 720
    page.window_width = int(1.5 * page.window_height)
    page.window_top = 100
    page.window_left = 720
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"

    # header
    image_path = Path(__file__).parent.joinpath(Path("assets/logo-192x192.png"))
    page.appbar = AppBar(
        leading=Image(src=image_path, height=40, width=40, border_radius=40),
        leading_width=56,
        toolbar_height=72,
        elevation=0,
        title=Text("OpenAndroidInstaller alpha version", style="displaySmall"),
        center_title=False,
        bgcolor="#00d886",
        actions=[
            Container(
                content=ElevatedButton(
                    icon=icons.BUG_REPORT_OUTLINED,
                    text="Report a bug",
                    on_click=lambda _: webbrowser.open(
                        "https://github.com/openandroidinstaller-dev/openandroidinstaller/issues"
                    ),
                ),
                padding=15,
                tooltip="Report an issue on github",
            )
        ],
    )

    # display a warnings banner
    def close_banner(e):
        page.banner.open = False
        page.update()

    page.banner = Banner(
        bgcolor=colors.AMBER_100,
        leading=Icon(icons.WARNING_AMBER_ROUNDED, color=colors.AMBER, size=40),
        content=Text(
            "Important: Please read through the instructions at least once before actually following them, so as to avoid any problems due to any missed steps!"
        ),
        actions=[
            TextButton("I understand", on_click=close_banner),
        ],
    )
    # TODO: disable the banner for now
    # page.banner.open = True
    # page.update()

    # create application instance
    app = MainView()

    # add application's root control to the page
    page.add(app)


flet.app(target=main, assets_dir="assets")
