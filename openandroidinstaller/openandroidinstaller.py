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

import os
import sys
import webbrowser
import regex as re
from pathlib import Path
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
    FloatingActionButton,
    VerticalDivider,
    Markdown,
    colors,
    icons,
)
from installer_config import Step, _load_config
from loguru import logger
from tool_utils import call_tool_with_command, search_device
from utils import AppState, get_download_link, image_recovery_works_with_device
from widgets import call_button, confirm_button, get_title, link_button

# Toggle to True for development purposes
DEVELOPMENT = False 
DEVELOPMENT_CONFIG = "sargo"  # "a3y17lte"  # "sargo"


PLATFORM = sys.platform
# Define asset paths
CONFIG_PATH = (
    Path(__file__).parent.joinpath(Path(os.sep.join(["assets", "configs"]))).resolve()
)
BIN_PATH = Path(__file__).parent.joinpath(Path("bin")).resolve()


class BaseView(UserControl):
    def __init__(self, image: str = "placeholder.png"):
        super().__init__()
        self.right_view = Column(expand=True)
        self.left_view = Column(
            width=600,
            controls=[Image(src=f"/assets/imgs/{image}")],
            expand=True,
            horizontal_alignment="center",
        )
        # main view row
        self.view = Row(
            [self.left_view, VerticalDivider(), self.right_view],
            alignment="spaceEvenly",
        )


class WelcomeView(BaseView):
    def __init__(
        self, on_confirm: Callable, load_config: Callable, page: Page, state: AppState
    ):
        super().__init__(image="connect-to-usb.png")
        self.on_confirm = on_confirm
        self.load_config = load_config
        self.page = page
        self.state = state

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
        )
        # checkbox to allow skipping unlocking the bootloader
        def check_bootloader_unlocked(e):
            """Enable skipping unlocking the bootloader if selected."""
            if self.bootloader_checkbox.value:
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

        self.bootloader_checkbox = Checkbox(
            label="Bootloader is already unlocked.",
            on_change=check_bootloader_unlocked,
            disabled=True,
        )

        # build up the main view
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
                        ElevatedButton(
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
                        self.bootloader_checkbox,
                    ]
                ),
                Row(
                    [
                        FilledButton(
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
        # map some detected device codes to their real code.
        device_code_mapping = {
            "C6603": "yuga",
        }
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
                device_code = device_code_mapping.get(device_code, device_code)
                self.device_name.value = device_code
            else:
                self.device_name.value = (
                    "No device detected! Connect to USB and try again."
                )

        # load the config, if a device is detected
        if device_code:
            self.device_name.value = device_code
            # load config from file
            device_name = self.load_config(device_code)

            # display success in the application
            if device_name:
                self.config_found_box.value = True
                self.continue_button.disabled = False
                self.bootloader_checkbox.disabled = False
                # overwrite the text field with the real name from the config
                self.device_name.value = f"{device_name} (code: {device_code})"
            else:
                # failed to load config
                logger.info(f"Failed to load config for {device_code}.")
                self.device_name.value = f"Failed to load config for {device_code}."
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
        state: AppState,
    ):
        super().__init__()
        self.on_confirm = on_confirm
        self.progressbar = progressbar
        self.pick_image_dialog = pick_image_dialog
        self.pick_recovery_dialog = pick_recovery_dialog
        self.selected_image = selected_image
        self.selected_recovery = selected_recovery
        self.state = state

    def build(self):
        self.download_link = get_download_link(
            self.state.config.metadata.get("devicecode", "ERROR")
        )
        self.confirm_button = confirm_button(self.on_confirm)
        self.confirm_button.disabled = True

        self.pick_recovery_dialog.on_result = self.enable_button_if_ready
        self.pick_image_dialog.on_result = self.enable_button_if_ready

        # attach hidden dialogues
        self.right_view.controls.append(self.pick_image_dialog)
        self.right_view.controls.append(self.pick_recovery_dialog)
        # add title and progressbar
        self.right_view.controls.append(get_title("Pick image and recovery files:"))
        self.right_view.controls.append(self.progressbar)
        # text row to show infos during the process
        self.info_field = Row()
        # if there is an available download, show the button to the page
        if self.download_link:
            self.right_view.controls.append(
                Column(
                    [
                        Text(
                            "You can bring your own image and recovery or you download the officially supported image and recovery file for your device here:"
                        ),
                        Row(
                            [
                                ElevatedButton(
                                    "Download",
                                    icon=icons.DOWNLOAD_OUTLINED,
                                    on_click=lambda _: webbrowser.open(
                                        self.download_link
                                    ),
                                    expand=True,
                                ),
                            ]
                        ),
                        Markdown(
                            f"""
The image file should look something like `lineage-19.1-20221101-nightly-{self.state.config.metadata.get('devicecode')}-signed.zip` 
and the recovery like `lineage-19.1-20221101-recovery-{self.state.config.metadata.get('devicecode')}.img` 
or `twrp-3.6.2_9-0-{self.state.config.metadata.get('devicecode')}.img`.
"""
                        ),
                        Divider(),
                    ]
                )
            )
        # attach the controls for uploading image and recovery
        self.right_view.controls.extend(
            [
                Text("Now select the operating system image and recovery:"),
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
                Text(
                    "If you selected both files and they work for your device you can continue."
                ),
                self.info_field,
                Row([self.confirm_button]),
            ]
        )
        return self.view

    def enable_button_if_ready(self, e):
        """Enable the confirm button if both files have been selected."""
        if (".zip" in self.selected_image.value) and (
            ".img" in self.selected_recovery.value
        ):
            if not image_recovery_works_with_device(
                device_code=self.state.config.metadata.get("devicecode"),
                image_path=self.state.image_path,
                recovery_path=self.state.recovery_path,
            ):
                # if image and recovery work for device allow to move on, otherwise display message
                self.info_field.controls = [
                    Text(
                        "Image and recovery don't work with the device. Please select different ones."
                    )
                ]
                self.right_view.update()
                return
            self.info_field.controls = []
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
        self.state = AppState()
        # initialize the progress bar indicator
        self.progress_bar = ProgressBar(
            width=600, color="#00d886", bgcolor="#eeeeee", bar_height=16
        )
        self.progress_bar.value = 0
        # create the main columns
        self.view = Column(expand=True, width=1200)
        # initialize global stuff
        # file pickers
        self.pick_image_dialog = FilePicker(on_result=self.pick_image_result)
        self.pick_recovery_dialog = FilePicker(on_result=self.pick_recovery_result)
        self.selected_image = Text("Selected image: ")
        self.selected_recovery = Text("Selected recovery: ")

        # text input
        self.inputtext = TextField(
            hint_text="your unlock code", expand=False
        )  # textfield for the unlock code

        # paths
        self.image_path = ""
        self.recovery_path = ""

        # create default starter views
        welcome = WelcomeView(
            on_confirm=self.confirm,
            load_config=self.load_config,
            page=self.page,
            state=self.state,
        )
        select_files = SelectFilesView(
            on_confirm=self.confirm,
            progressbar=self.progress_bar,
            pick_image_dialog=self.pick_image_dialog,
            pick_recovery_dialog=self.pick_recovery_dialog,
            selected_image=self.selected_image,
            selected_recovery=self.selected_recovery,
            state=self.state,
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
                self.state.num_total_steps + 2
            )  # don't show on the first step
            self.num_steps += 1  # increase the step counter
        # if there are default views left, display them first
        if self.default_views:
            self.view.controls.append(self.default_views.pop())
        elif self.state.steps:
            self.view.controls.append(
                StepView(
                    step=self.state.steps.pop(0),
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

    def load_config(self, device_code: str) -> Optional[str]:
        """Function to load a config file from device code."""
        self.config = _load_config(device_code, CONFIG_PATH)
        self.state.config = self.config
        if self.config:
            self.state.steps = (
                self.config.unlock_bootloader
                + self.config.flash_recovery
                + self.config.install_os
            )
            self.state.num_total_steps = len(self.state.steps)
            return self.config.metadata.get("devicename", "No device name in config.")

    def pick_image_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        self.selected_image.value = (
            self.selected_image.value.split(":")[0] + f": {path}"
        )
        if e.files:
            self.image_path = e.files[0].path
            self.state.image_path = e.files[0].path
            logger.info(f"Selected image from {self.image_path}")
        else:
            logger.info("No image selected.")
        self.selected_image.update()

    def pick_recovery_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        self.selected_recovery.value = (
            self.selected_recovery.value.split(":")[0] + f": {path}"
        )
        if e.files:
            self.recovery_path = e.files[0].path
            self.state.recovery_path = e.files[0].path
            logger.info(f"Selected recovery from {self.recovery_path}")
        else:
            logger.info("No image selected.")
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
        elif self.step.type == "link_button_with_confirm":
            self.confirm_button = confirm_button(self.on_confirm)
            self.right_view.controls.extend(
                [Row([link_button(self.step.link, "Open Link"), self.confirm_button])]
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
        # replace placeholders by the required values
        command = command.replace("<recovery>", self.recovery_path)
        command = command.replace("<image>", self.image_path)
        command = command.replace("<inputtext>", self.inputtext.value)

        # display a progress ring to show something is happening
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
        if not success:
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
    page.window_height = 780
    page.window_width = int(1.77 * page.window_height)
    page.window_top = 100
    page.window_left = 120
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"

    # header
    page.appbar = AppBar(
        leading=Image(
            src=f"/assets/logo-192x192.png", height=40, width=40, border_radius=40
        ),
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
            "These instructions only work if you follow every section and step precisely. Do not continue after something fails!"
        ),
        actions=[
            TextButton("I understand", on_click=close_banner),
        ],
    )
    page.banner.open = True
    page.update()

    # create application instance
    app = MainView()

    # add a button that restarts the process
    def restart_process(e):
        logger.info("Restarted the process. Reset everything.")
        page.controls.pop()
        app = MainView()
        page.add(app)
        page.update()

    page.floating_action_button = FloatingActionButton(
        text="Restart the process",
        icon=icons.RESTART_ALT_OUTLINED,
        tooltip="You can safely restart if you missed a step or didn't make it.",
        on_click=restart_process,
    )

    # add application's root control to the page
    page.add(app)


flet.app(target=main, assets_dir="assets")
