from functools import partial
from os import path
from subprocess import STDOUT, CalledProcessError, call, check_output
from time import sleep
from turtle import width
from typing import Callable, List

import flet
from flet import (AppBar, Banner, Column, Container, Divider, ElevatedButton,
                  FilePicker, FilePickerResultEvent, Icon, Image, Page,
                  ProgressBar, ProgressRing, Row, Text, TextButton, TextField,
                  UserControl, View, alignment, colors, icons)
from installer_config import InstallerConfig, Step
from widgets import call_button, confirm_button, get_title

CONFIG_PATH = path.abspath(path.join(path.dirname(__file__), "assets/configs/"))


class WelcomeView(UserControl):
    def __init__(
        self, on_confirm: Callable, load_config: Callable, progressbar: ProgressBar
    ):
        super().__init__()
        self.on_confirm = on_confirm
        self.load_config = load_config
        self.progressbar = progressbar
        self.view = Column(width=400)

    def build(self):
        self.view.controls.extend(
            [
                get_title("Welcome to the OpenAndroidInstaller"),
                self.progressbar,
                Text(
                    "Before you continue, make sure your devices is on the latest system update."
                ),
                Divider(),
                Text(
                    """Enable USB debugging on your device by enabling developer options. To do this, tap seven times on the build number in the System-Menu in Settings. Then in developer options, toggle OEM unlocking and USB-Debugging."""
                ),
                Row(
                    [
                        ElevatedButton(
                            "Search device",
                            on_click=self.search_devices,
                            icon=icons.PHONE_ANDROID,
                        )
                    ],
                    alignment="center",
                ),
            ]
        )
        return self.view

    def search_devices(self, e):
        try:
            # read device properties
            output = check_output(
                [
                    "adb",
                    "shell",
                    "dumpsys",
                    "bluetooth_manager",
                    "|",
                    "grep",
                    "'name:'",
                    "|",
                    "cut",
                    "-c9-",
                ],
                stderr=STDOUT,
            ).decode()
            self.view.controls.append(Text(f"Detected: {output}"))
            # load config from file
            path = f"{CONFIG_PATH}/{output.strip()}.yaml"
            load_config_success = self.load_config(path)
            if load_config_success:
                self.view.controls.append(Text(f"Installer configuration found."))
                self.view.controls.append(
                    Row(
                        [
                            ElevatedButton(
                                "Confirm and continue",
                                on_click=self.on_confirm,
                                icon=icons.NEXT_PLAN_OUTLINED,
                            )
                        ],
                        alignment="center",
                    )
                )
            else:
                self.view.controls.append(Text(f"No matching config found."))
                # show alternative configs here
                # select a new path and load again
                pass
        except CalledProcessError:
            output = "No device detected!"
            self.view.controls.append(Text(f"{output}"))
        self.view.update()


class SelectFilesView(UserControl):
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
        self.view = Column(width=400)

    def build(self):
        self.view.controls.append(self.pick_image_dialog)
        self.view.controls.append(self.pick_recovery_dialog)
        self.view.controls.extend(
            [
                get_title("Pick image and recovery"),
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
                        ),
                        self.selected_image,
                    ]
                ),
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
                        ),
                        self.selected_recovery,
                    ]
                ),
                confirm_button("Done?", self.on_confirm),
            ]
        )
        return self.view


class MainView(UserControl):
    def __init__(self):
        super().__init__()
        self.config = None
        # initialize the progress bar indicator
        self.progress_bar = ProgressBar(
            width=400, color="#00d886", bgcolor="#eeeeee", bar_height=16
        )
        self.progress_bar.value = 0
        # create the main column
        self.view = Column()
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
            on_confirm=self.confirm,
            load_config=self.load_config,
            progressbar=self.progress_bar,
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
        # keep track of the number of steps
        self.num_steps = len(self.default_views)

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
                len(self.config.steps) + 2
            )  # don't show on the first step
            self.num_steps += 1  # increase the step counter
        # if there are default views left, display them first
        if self.default_views:
            self.view.controls.append(self.default_views.pop())
        else:
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
        self.view.update()

    def load_config(self, path: str):
        """Function to load a config file from path."""
        try:
            self.config = InstallerConfig.from_file(path)
            return True
        except FileNotFoundError:
            return False

    def pick_image_result(self, e: FilePickerResultEvent):
        self.selected_image.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.image_path = e.files[0].path
        self.selected_image.update()

    def pick_recovery_result(self, e: FilePickerResultEvent):
        self.selected_recovery.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        self.recovery_path = e.files[0].path
        self.selected_recovery.update()


class StepView(UserControl):
    def __init__(
        self,
        step: Step,
        on_confirm: Callable,
        progressbar: ProgressBar,
        inputtext: TextField,
        image_path: str,
        recovery_path: str,
    ):
        super().__init__()
        self.step = step
        self.on_confirm = on_confirm
        self.progressbar = progressbar
        self.inputtext = inputtext
        self.image_path = image_path
        self.recovery_path = recovery_path

        self.view = Column(width=400)

    def build(self):
        """Create the content of a view from step."""
        self.view.controls = [get_title(f"{self.step.title}"), self.progressbar]
        # basic view depending on step.type
        if self.step.type == "confirm_button":
            self.view.controls.append(
                confirm_button(self.step.content, self.on_confirm)
            )
        elif self.step.type == "call_button":
            self.view.controls.append(
                call_button(
                    self.step.content, self.call_to_phone, command=self.step.command
                )
            )
        elif self.step.type == "call_button_with_input":
            self.view.controls.extend(
                [
                    self.inputtext,
                    call_button(
                        self.step.content, self.call_to_phone, command=self.step.command
                    ),
                ]
            )
        elif self.step.type == "text":
            self.view.controls.append(Text(self.step.content))
        else:
            raise Exception(f"Unknown step type: {self.step.type}")

        # if skipping is allowed add a button to the view
        if self.step.allow_skip:
            self.view.controls.append(
                confirm_button("Already done?", self.on_confirm, confirm_text="Skip")
            )
        return self.view

    def call_to_phone(self, e, command: str):
        command = command.replace("<recovery>", self.recovery_path)
        command = command.replace("<image>", self.image_path)
        command = command.replace("<inputtext>", self.inputtext.value)
        self.view.controls.append(
            Row(
                [ProgressRing(color="#00d886")],  # , Text("Wait for completion...")],
                alignment="center",
            )
        )
        self.view.update()
        res = call(f"{command}", shell=True)
        if res != 0:
            self.view.controls.pop()
            self.view.controls.append(Text("Command {command} failed!"))
        else:
            sleep(5)
            self.view.controls.pop()  # pop the progress ring
            self.view.controls.append(
                ElevatedButton("Confirm and continue", on_click=self.on_confirm)
            )
        self.view.update()


def main(page: Page):
    # Configure the application base page
    page.title = "OpenAndroidInstaller"
    page.window_width = 480
    page.window_height = 640
    page.window_top = 100
    page.window_left = 720
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"

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
    page.banner.open = True

    page.update()

    # create application instance
    app = MainView()

    # add application's root control to the page
    page.add(app)


flet.app(target=main, assets_dir="assets")
