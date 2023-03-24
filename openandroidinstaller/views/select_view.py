"""Contains the select files view."""

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
from loguru import logger
from typing import Callable

from flet import (
    Column,
    Divider,
    ElevatedButton,
    OutlinedButton,
    FilledButton,
    Markdown,
    Row,
    Text,
    colors,
    icons,
    TextButton,
    AlertDialog,
    FilePicker,
    FilePickerResultEvent,
)
from flet.buttons import CountinuosRectangleBorder

from views import BaseView
from app_state import AppState
from widgets import get_title, confirm_button
from utils import get_download_link, image_works_with_device, recovery_works_with_device


class SelectFilesView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
        on_back: Callable,
    ):
        super().__init__(state=state)
        self.on_confirm = on_confirm
        self.on_back = on_back

        self.init_visuals()

    def init_visuals(
        self,
    ):
        """Initialize the stateful visual elements of the view."""
        # dialog box to explain OS images and recovery
        self.dlg_explain_images = AlertDialog(
            modal=True,
            title=Text("What is an OS image and recovery and why do I need it?"),
            content=Markdown(
                """## OS image or ROM
An operating system (OS) is system software that manages computer hardware,
software resources, and provides common services for computer programs. 
Popular, custom operating systems for mobile devices based on Android are 
- [LineageOS](https://lineageos.org/)
- [/e/OS](https://e.foundation/e-os/) or
- [LineageOS for microG](https://lineage.microg.org/)
- and many others.

Often, the related OS images are called 'ROM'. 'ROM' stands for *R*ead-*o*nly *m*emory,
which is a type of non-volatile memory used in computers for storing software that is
rarely changed during the life of the system, also known as firmware.

## Recovery Image
A custom recovery is used for installing custom software on your device.
This custom software can include smaller modifications like rooting your device or even
replacing the firmware of the device with a completely custom ROM.

OpenAndroidInstaller works with the [TWRP recovery project](https://twrp.me/about/).""",
                on_tap_link=lambda e: self.page.launch_url(e.data),
            ),
            actions=[
                TextButton("Close", on_click=self.close_close_explain_images_dlg),
            ],
            actions_alignment="end",
            shape=CountinuosRectangleBorder(radius=0),
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
        # back button
        self.back_button = ElevatedButton(
            "Back",
            on_click=self.on_back,
            icon=icons.ARROW_BACK,
            expand=True,
        )

    def build(self):
        self.clear()

        # download link
        self.download_link = get_download_link(
            self.state.config.metadata.get("device_code", "NOTFOUND")
        )

        # attach hidden dialogues
        self.right_view.controls.append(self.pick_image_dialog)
        self.right_view.controls.append(self.pick_recovery_dialog)

        # create help/info button to show the help dialog
        info_button = OutlinedButton(
            "What is this?",
            on_click=self.open_explain_images_dlg,
            expand=True,
            icon=icons.HELP_OUTLINE_OUTLINED,
            icon_color=colors.DEEP_ORANGE_500,
            tooltip="Get more details on custom operating system images and recoveries.",
        )

        # add title
        self.right_view_header.controls.append(
            get_title(
                "Now pick an OS image and a recovery file:",
                info_button=info_button,
                step_indicator_img="steps-header-select.png",
            )
        )

        # text row to show infos during the process
        self.info_field = Row()
        # if there is an available download, show the button to the page
        if self.download_link:
            twrp_download_link = f"https://dl.twrp.me/{self.state.config.twrp_link if self.state.config.twrp_link else self.state.config.device_code}"
            self.right_view.controls.append(Divider())
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
                                        twrp_download_link
                                    ),
                                    expand=True,
                                ),
                            ]
                        ),
                        Divider(),
                    ]
                )
            )
        # attach the controls for uploading image and recovery
        self.right_view.controls.extend(
            [
                Text("Select an OS image:", style="titleSmall"),
                Markdown(
                    f"""
The image file should look something like `lineage-19.1-20221101-nightly-{self.state.config.device_code}-signed.zip`."""
                ),
                Row(
                    [
                        FilledButton(
                            "Pick OS image",
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
                Divider(),
                Text("Select a TWRP recovery image:", style="titleSmall"),
                Markdown(
                    f"""
The recovery image should look something like `twrp-3.7.0_12-0-{self.state.config.device_code}.img`.

**Note:** This tool **only supports TWRP recoveries**.""",
                    extension_set="gitHubFlavored",
                ),
                Row(
                    [
                        FilledButton(
                            "Pick TWRP recovery file",
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
                self.info_field,
                Row([self.back_button, self.confirm_button]),
            ]
        )
        return self.view

    def open_explain_images_dlg(self, e):
        """Open the dialog to explain OS and recovery image."""
        self.page.dialog = self.dlg_explain_images
        self.dlg_explain_images.open = True
        self.page.update()

    def close_close_explain_images_dlg(self, e):
        """Close the dialog to explain OS and recovery image."""
        self.dlg_explain_images.open = False
        self.page.update()

    def pick_image_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # update the textfield with the name of the file
        self.selected_image.value = (
            self.selected_image.value.split(":")[0] + f": {path}"
        )
        if e.files:
            self.image_path = e.files[0].path
            self.state.image_path = e.files[0].path
            logger.info(f"Selected image from {self.image_path}")
        else:
            logger.info("No image selected.")
        # check if the image works with the device and show the filename in different colors accordingly
        if e.files:
            if image_works_with_device(
                supported_device_codes=self.state.config.supported_device_codes,
                image_path=self.state.image_path,
            ):
                self.selected_image.color = colors.GREEN
            else:
                self.selected_image.color = colors.RED
        # update
        self.selected_image.update()

    def pick_recovery_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # update the textfield with the name of the file
        self.selected_recovery.value = (
            self.selected_recovery.value.split(":")[0] + f": {path}"
        )
        if e.files:
            self.recovery_path = e.files[0].path
            self.state.recovery_path = e.files[0].path
            logger.info(f"Selected recovery from {self.recovery_path}")
        else:
            logger.info("No image selected.")
        # check if the recovery works with the device and show the filename in different colors accordingly
        if e.files:
            device_code = self.state.config.device_code
            if recovery_works_with_device(
                device_code=device_code, recovery_path=self.state.recovery_path
            ):
                self.selected_recovery.color = colors.GREEN
            else:
                self.selected_recovery.color = colors.RED
        # update
        self.selected_recovery.update()

    def enable_button_if_ready(self, e):
        """Enable the confirm button if both files have been selected."""
        if (".zip" in self.selected_image.value) and (
            ".img" in self.selected_recovery.value
        ):
            device_code = self.state.config.device_code
            if not (
                image_works_with_device(
                    supported_device_codes=self.state.config.supported_device_codes,
                    image_path=self.state.image_path,
                )
                and recovery_works_with_device(
                    device_code=device_code, recovery_path=self.state.recovery_path
                )
            ):
                # if image and recovery work for device allow to move on, otherwise display message
                logger.error(
                    "Image and recovery don't work with the device. Please select different ones."
                )
                self.info_field.controls = [
                    Text(
                        "Image and/or recovery don't work with the device. Make sure you use a TWRP-based recovery.",
                        color=colors.RED,
                        weight="bold",
                    )
                ]
                self.confirm_button.disabled = True
                self.right_view.update()
                return
            logger.info("Image and recovery work with the device. You can continue.")
            self.info_field.controls = []
            self.confirm_button.disabled = False
            self.right_view.update()
        else:
            self.confirm_button.disabled = True
