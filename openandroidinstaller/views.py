"""This file contains the flet views of the application."""

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

import webbrowser
from time import sleep
from typing import Callable
from pathlib import Path
from loguru import logger

from flet import (
    AlertDialog,
    alignment,
    Checkbox,
    Switch,
    Card,
    Column,
    Container,
    Divider,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilledButton,
    Image,
    Markdown,
    ProgressBar,
    Row,
    Text,
    TextButton,
    TextField,
    UserControl,
    VerticalDivider,
    colors,
    icons,
)

from app_state import AppState
from installer_config import Step
from tool_utils import (
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
    search_device,
)
from utils import get_download_link, image_recovery_works_with_device
from widgets import call_button, confirm_button, get_title, link_button


class BaseView(UserControl):
    def __init__(self, state: AppState, image: str = "placeholder.png"):
        super().__init__()
        self.state = state
        # right part of the display, add content here.
        self.right_view = Column(expand=True)
        # left part of the display: used for displaying the images
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


class RequirementsView(BaseView):
    """View to display requirements and ask for confirmation."""

    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state, image="requirements-default.png")
        self.on_confirm = on_confirm

    def build(self):
        self.continue_button = ElevatedButton(
            "Continue",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )

        # build up the main view
        self.right_view.controls.extend(
            [
                get_title("Check the Requirements"),
                Text(
                    "Before continuing you need to check some requirements to progress. Please read the instructions and check the boxes if everything is fine."
                ),
                Divider(),
            ]
        )
        self.checkboxes = []

        def enable_continue_button(e):
            """Enable the continue button if all checkboxes are ticked."""
            for checkbox in self.checkboxes:
                if not checkbox.value:
                    self.continue_button.disabled = True
                    return
            logger.info("All requirements ticked. Allow to continue")
            self.continue_button.disabled = False
            self.right_view.update()

        # check if there are additional requirements given in the config
        if self.state.config.requirements:
            # android version
            required_android_version = self.state.config.requirements.get("android")
            if required_android_version:
                android_checkbox = Checkbox(
                    label="The required android version is installed. (Or I know the risk of continuing)",
                    on_change=enable_continue_button,
                )
                android_version_check = Card(
                    Container(
                        content=Column(
                            [
                                Markdown(
                                    f"""
#### Android Version {required_android_version}:
Before following these instructions please ensure that the device is currently using Android {required_android_version} firmware.
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
                self.right_view.controls.append(android_version_check)

            # firmware version
            required_firmware_version = self.state.config.requirements.get("firmware")
            if required_firmware_version:
                firmware_checkbox = Checkbox(
                    label="The required firmware version is installed. (Or I know the risk of continuing)",
                    on_change=enable_continue_button,
                )
                firmware_version_check = Card(
                    Container(
                        content=Column(
                            [
                                Markdown(
                                    f"""
#### Firmware Version {required_firmware_version}:
Before following these instructions please ensure that the device is on firmware version {required_firmware_version}.
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
                self.right_view.controls.append(firmware_version_check)

        # default requirements: battery level
        battery_checkbox = Checkbox(
            label="The battery level is over 80%.",
            on_change=enable_continue_button,
        )
        battery_version_check = Card(
            Container(
                content=Column(
                    [
                        Markdown(
                            f"""
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
        self.checkboxes.append(battery_checkbox)
        self.right_view.controls.append(battery_version_check)

        # default requirement: disable lock code and fingerprint
        lock_checkbox = Checkbox(
            label="No lock code or fingerprint lock enabled.",
            on_change=enable_continue_button,
        )
        lock_check = Card(
            Container(
                content=Column(
                    [
                        Markdown(
                            f"""
#### Disable all device lock codes and fingerprint locks.
            """
                        ),
                        lock_checkbox,
                    ]
                ),
                padding=10,
            ),
        )
        self.checkboxes.append(lock_checkbox)
        self.right_view.controls.append(lock_check)

        # add the final confirm and continue button
        self.right_view.controls.append(Row([self.continue_button], alignment="center"))
        return self.view


class WelcomeView(BaseView):
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

        # switch to enable advanced output - here it means show terminal input/output in tool
        def check_advanced_switch(e):
            """Check the box to enable advanced output."""
            if self.advanced_switch.value:
                logger.info("Enable advanced output.")
                self.state.advanced = True
            else:
                logger.info("Disable advanced output.")
                self.state.advanced = False

        self.advanced_switch = Switch(
            label="Advanced output",
            on_change=check_advanced_switch,
            disabled=False,
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
- to not store the backup not the phone! 

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
                        Row([self.bootloader_switch, self.advanced_switch]),
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
                device_code = device_code_mapping.get(device_code, device_code)
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


class SelectFilesView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state)
        self.on_confirm = on_confirm

    def build(self):
        self.download_link = get_download_link(
            self.state.config.metadata.get("devicecode", "ERROR")
        )
        # initialize file pickers
        self.pick_image_dialog = FilePicker(on_result=self.pick_image_result)
        self.pick_recovery_dialog = FilePicker(on_result=self.pick_recovery_result)
        self.selected_image = Text("Selected image: ")
        self.selected_recovery = Text("Selected recovery: ")

        # initialize and manage button state.
        self.confirm_button = confirm_button(self.on_confirm)
        self.confirm_button.disabled = True
        self.pick_recovery_dialog.on_result = self.enable_button_if_ready
        self.pick_image_dialog.on_result = self.enable_button_if_ready

        # attach hidden dialogues
        self.right_view.controls.append(self.pick_image_dialog)
        self.right_view.controls.append(self.pick_recovery_dialog)
        # add title and progressbar
        self.right_view.controls.append(get_title("Pick image and recovery files:"))
        self.right_view.controls.append(self.state.progressbar)
        # text row to show infos during the process
        self.info_field = Row()
        # if there is an available download, show the button to the page
        if self.download_link:
            self.right_view.controls.append(
                Column(
                    [
                        Text(
                            "You can bring your own image and recovery or you download the officially supported image file for your device here:"
                        ),
                        Row(
                            [
                                ElevatedButton(
                                    "Download LineageOS image",
                                    icon=icons.DOWNLOAD_OUTLINED,
                                    on_click=lambda _: webbrowser.open(
                                        self.download_link
                                    ),
                                    expand=True,
                                ),
                                ElevatedButton(
                                    "Download TWRP recovery",
                                    icon=icons.DOWNLOAD_OUTLINED,
                                    on_click=lambda _: webbrowser.open(
                                        f"https://dl.twrp.me/{self.state.config.metadata.get('devicecode')}"
                                    ),
                                    expand=True,
                                ),
                            ]
                        ),
                        Markdown(
                            f"""
The image file should look something like `lineage-19.1-20221101-nightly-{self.state.config.metadata.get('devicecode')}-signed.zip` 
and the recovery like `twrp-3.6.2_9-0-{self.state.config.metadata.get('devicecode')}.img`. Note that this tool only supports TWRP recoveries for now.
"""
                        ),
                        Divider(),
                    ]
                )
            )
        # attach the controls for uploading image and recovery
        self.right_view.controls.extend(
            [
                Text(
                    "Now select the operating system image and recovery (note, that only TWRP recoveries are supported):"
                ),
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
                logger.error(
                    "Image and recovery don't work with the device. Please select different ones."
                )
                self.info_field.controls = [
                    Text(
                        "Image and recovery don't work with the device. Please select different ones."
                    )
                ]
                self.right_view.update()
                return
            logger.info("Image and recovery work with the device. You can continue.")
            self.info_field.controls = []
            self.confirm_button.disabled = False
            self.right_view.update()
        else:
            self.confirm_button.disabled = True


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
            self.right_view.controls.append(
                Row([self.call_button, self.confirm_button]),
            )
            # add terminal box if enabled
            if self.state.advanced:
                self.right_view.controls.append(Row([self.terminal_box]))
        elif self.step.type == "call_button_with_input":
            self.confirm_button.disabled = True
            self.call_button = call_button(
                self.call_to_phone, command=self.step.command
            )
            self.right_view.controls.extend(
                [self.inputtext, Row([self.call_button, self.confirm_button])]
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
        self.right_view.controls.append(
            Row(
                [
                    ProgressBar(
                        width=600, color="#00d886", bgcolor="#eeeeee", bar_height=16
                    )
                ],
                alignment="center",
            ),
        )
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
                if self.state.advanced and (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "adb_sideload":
            for line in adb_sideload(
                bin_path=self.state.bin_path, target=self.state.image_path
            ):
                if self.state.advanced and (type(line) == str) and line.strip():
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
                if self.state.advanced and (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "fastboot_flash_recovery":
            for line in fastboot_flash_recovery(
                bin_path=self.state.bin_path, recovery=self.state.recovery_path
            ):
                if self.state.advanced and (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "fastboot_unlock_with_code":
            for line in fastboot_unlock_with_code(
                bin_path=self.state.bin_path, unlock_code=self.inputtext.value
            ):
                if self.state.advanced and (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        elif command == "heimdall_flash_recovery":
            for line in heimdall_flash_recovery(
                bin_path=self.state.bin_path, recovery=self.state.recovery_path
            ):
                if self.state.advanced and (type(line) == str) and line.strip():
                    self.terminal_box.content.controls.append(
                        Text(f">{line.strip()}", selectable=True)
                    )
                    self.terminal_box.update()
            success = line
        else:
            logger.error(f"Unknown command type: {command}. Stopping.")
            raise Exception(f"Unknown command type: {command}. Stopping.")

        # update the view accordingly
        if not success:
            # enable call button to retry
            self.call_button.disabled = False
            # pop the progress bar
            self.right_view.controls.pop()
            # also remove the last error text if it happened
            if isinstance(self.right_view.controls[-1], Text):
                self.right_view.controls.pop()
            self.right_view.controls.append(
                Text(
                    f"Command {command} failed! Try again or make sure everything is setup correctly."
                )
            )
        else:
            sleep(5)  # wait to make sure everything is fine
            logger.success(f"Command {command} run successfully. Allow to continue.")
            # pop the progress bar
            self.right_view.controls.pop()
            # emable the confirm buton and disable the call button
            self.confirm_button.disabled = False
            self.call_button.disabled = True
        self.view.update()


class SuccessView(BaseView):
    def __init__(self, state: AppState):
        super().__init__(state=state, image="success.png")

    def build(
        self,
    ):
        self.right_view.controls = [
            get_title("Installation completed successfully!"),
            self.state.progressbar,
            Text("Now your devices boots into the new OS. Have fun with it!"),
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
