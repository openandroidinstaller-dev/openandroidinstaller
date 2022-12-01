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
    Markdown,
    Row,
    Text,
    icons,
    TextButton,
    AlertDialog,
    FilePicker,
    FilePickerResultEvent,
)

from views import BaseView
from app_state import AppState
from widgets import get_title, confirm_button
from utils import (
    get_download_link,
    image_recovery_works_with_device,
)


class SelectFilesView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state)
        self.on_confirm = on_confirm

    def build(self):
        # dialog box to explain OS images and recovery
        self.dlg_explain_images = AlertDialog(
            modal=True,
            title=Text("What is an OS image and recovery and why do I need it?"),
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

        # download link
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
        self.right_view.controls.append(get_title("Now pick an OS image and a recovery file:"))
        self.right_view.controls.append(self.state.progressbar)
        # button to show the explainaition dialoge
        self.right_view.controls.append(
            Row(
                    [
                        ElevatedButton(
                            "What is an OS image and a recovery file?",
                            on_click=self.open_explain_images_dlg,
                            expand=True,
                            tooltip="Get some details about those files and why you need them.",
                        )
                    ]
                )
        )

        # text row to show infos during the process
        self.info_field = Row()
        # if there is an available download, show the button to the page
        if self.download_link:
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

    def open_explain_images_dlg(self, e):
        """Open the dialog to explain OS and recovery image."""
        self.page.dialog = self.dlg_explain_images
        self.dlg_explain_images.open = True
        self.page.update()

    def close_developer_options_dlg(self, e):
        """Close the dialog to explain OS and recovery image."""
        self.dlg_explain_images.open = False
        self.page.update()

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
