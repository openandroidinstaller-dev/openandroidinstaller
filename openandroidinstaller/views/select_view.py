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
    Row,
    colors,
    icons,
    TextButton,
    AlertDialog,
    FilePicker,
    FilePickerResultEvent,
    Checkbox,
)
from flet_core.buttons import CountinuosRectangleBorder

from styles import (
    Text,
    Markdown,
)
from views import BaseView
from app_state import AppState
from widgets import get_title, confirm_button
from utils import (
    get_download_link,
    image_works_with_device,
    recovery_works_with_device,
    image_sdk_level,
)


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
- [LineageOS](https://lineageos.org)
- [/e/OS](https://e.foundation/e-os) or
- [LineageOS for microG](https://lineage.microg.org)
- and many others.

Often, the related OS images are called 'ROM'. 'ROM' stands for *R*ead-*o*nly *m*emory,
which is a type of non-volatile memory used in computers for storing software that is
rarely changed during the life of the system, also known as firmware.

## Recovery Image
A custom recovery is used for installing custom software on your device.
This custom software can include smaller modifications like rooting your device or even
replacing the firmware of the device with a completely custom ROM.

OpenAndroidInstaller works with the [TWRP recovery project](https://twrp.me/about).""",
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
        self.pick_dtbo_dialog = FilePicker(on_result=self.pick_dtbo_result)
        self.pick_vbmeta_dialog = FilePicker(on_result=self.pick_vbmeta_result)
        self.pick_super_empty_dialog = FilePicker(
            on_result=self.pick_super_empty_result
        )

        self.selected_image = Text("Selected image: ")
        self.selected_recovery = Text("Selected recovery: ")
        self.selected_dtbo = Checkbox(
            fill_color=colors.RED, value=None, disabled=True, tristate=True
        )
        self.selected_vbmeta = Checkbox(
            fill_color=colors.RED, value=None, disabled=True, tristate=True
        )
        self.selected_super_empty = Checkbox(
            fill_color=colors.RED, value=None, disabled=True, tristate=True
        )

        # initialize and manage button state.
        self.confirm_button = confirm_button(self.on_confirm)
        self.confirm_button.disabled = True
        self.pick_recovery_dialog.on_result = self.enable_button_if_ready
        self.pick_image_dialog.on_result = self.enable_button_if_ready
        self.pick_dtbo_dialog.on_result = self.enable_button_if_ready
        self.pick_vbmeta_dialog.on_result = self.enable_button_if_ready
        self.pick_super_empty_dialog.on_result = self.enable_button_if_ready
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
        self.right_view.controls.extend(
            [
                self.pick_image_dialog,
                self.pick_recovery_dialog,
                self.pick_dtbo_dialog,
                self.pick_vbmeta_dialog,
                self.pick_super_empty_dialog,
            ]
        )

        # create help/info button to show the help dialog for the image and recovery selection
        explain_images_button = OutlinedButton(
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
                info_button=explain_images_button,
                step_indicator_img="steps-header-select.png",
            )
        )

        # text row to show infos during the process
        self.info_field = Row()
        # column to insert the additional image selection controls if needed
        self.additional_image_selection = Column()

        # Device specific notes
        notes = self.get_notes()
        if notes:
            self.right_view.controls.extend(
                [
                    Text(
                        "Important notes for your device",
                        style="titleSmall",
                        color=colors.RED,
                        weight="bold",
                    ),
                    Markdown(notes),
                ]
            )

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
                self.additional_image_selection,
            ]
        )

        # attach the bottom buttons
        self.right_view.controls.extend(
            [
                self.info_field,
                Row([self.back_button, self.confirm_button]),
            ]
        )
        return self.view

    def get_notes(self) -> str:
        """Prepare and get notes for the specific device from config.

        These notes should be displayed to the user.
        """
        notes = []

        brand = self.state.config.metadata.get("brand", "")
        if brand in "xiaomi":
            notes.append(
                "- If something goes wrong, you can reinstall MiUI here:\n<https://xiaomifirmwareupdater.com/>\n"
            )
        elif brand in "poco":
            notes.append(
                f"- If something goes wrong, you can reinstall MiUI here:\n<https://xiaomifirmwareupdater.com/miui/{self.state.config.device_code}/>\n"
            )

        # this should be used as little as possible!
        if self.state.config.metadata.get("untested", False):
            notes.append(
                "- **This device has not been tested with OpenAndroidInstaller yet.** The installation can go wrong. You may have to finish the installation process with command line. If you test, please report the result on GitHub."
            )

        notes.extend(
            f"- {note}" for note in self.state.config.metadata.get("notes", [])
        )
        return "\n\n".join(notes)

    def toggle_additional_image_selection(self):
        """Toggle the visibility of the additional image selection controls."""
        # dialogue box to explain additional required images
        self.dlg_explain_additional_images = AlertDialog(
            modal=True,
            title=Text("Why do I need additional images and where do I get them?"),
            content=Markdown(
                f"""## About additional images
Some devices require additional images to be flashed before the recovery and OS image can be flashed.
Not all images explained below are required for all devices. The installer will tell you which images are required for your device.

### dtbo.img
The `dtbo.img` is a partition image that contains the device tree overlay.

### vbmeta.img
The `vbmeta.img` is a partition image that contains the verified boot metadata.
This is required to prevent issues with the verified boot process.

### super_empty.img
The `super_empty.img` is used to wipe the super partition. This is required to
prevent issues with the super partition when flashing a new ROM.

### vendor_boot.img
The `vendor_boot.img` is a partition image that contains the vendor boot image.

## Where do I get these images?
You can download the required images for your device from the [LineageOS downloads page](https://download.lineageos.org/devices/{self.state.config.device_code}/builds).
If this download page does not contain the required images, you can try to find them on the [XDA developers forum](https://forum.xda-developers.com/).
                """,
                auto_follow_links=True,
            ),
            actions=[
                TextButton(
                    "Close", on_click=self.close_close_explain_additional_images_dlg
                ),
            ],
            actions_alignment="end",
            shape=CountinuosRectangleBorder(radius=0),
        )

        # create help/info button to show the help dialog for the image and recovery selection
        explain_additional_images_button = OutlinedButton(
            "Why do I need this and where do I get it?",
            on_click=self.open_explain_additional_images_dlg,
            expand=True,
            icon=icons.HELP_OUTLINE_OUTLINED,
            icon_color=colors.DEEP_ORANGE_500,
            tooltip="Get more details on additional images and download links.",
        )

        # attach the controls for uploading others partitions, like dtbo, vbmeta & super_empty
        additional_image_selection = []
        if self.state.config.metadata["additional_steps"]:
            additional_image_selection.extend(
                [
                    Row(
                        [
                            Text(
                                "Select required additional images:", style="titleSmall"
                            ),
                            explain_additional_images_button,
                        ]
                    ),
                    Markdown(
                        """
Your selected device and ROM requires flashing of additional partitions. Please select the required images below.

Make sure the file is for **your exact phone model!**""",
                    ),
                ]
            )
        if "dtbo" in self.state.config.metadata["additional_steps"]:
            self.selected_dtbo.value = False
            additional_image_selection.extend(
                [
                    Row(
                        [
                            FilledButton(
                                "Pick `dtbo.img` image",
                                icon=icons.UPLOAD_FILE,
                                on_click=lambda _: self.pick_dtbo_dialog.pick_files(
                                    allow_multiple=False,
                                    file_type="custom",
                                    allowed_extensions=["img"],
                                ),
                                expand=True,
                            ),
                            self.selected_dtbo,
                        ]
                    ),
                ]
            )
        if "vbmeta" in self.state.config.metadata["additional_steps"]:
            self.selected_vbmeta.value = False
            additional_image_selection.extend(
                [
                    Row(
                        [
                            FilledButton(
                                "Pick `vbmeta.img` image",
                                icon=icons.UPLOAD_FILE,
                                on_click=lambda _: self.pick_vbmeta_dialog.pick_files(
                                    allow_multiple=False,
                                    file_type="custom",
                                    allowed_extensions=["img"],
                                ),
                                expand=True,
                            ),
                            self.selected_vbmeta,
                        ]
                    ),
                ]
            )
        if "super_empty" in self.state.config.metadata["additional_steps"]:
            self.selected_super_empty.value = False
            additional_image_selection.extend(
                [
                    Row(
                        [
                            FilledButton(
                                "Pick `super_empty.img` image",
                                icon=icons.UPLOAD_FILE,
                                on_click=lambda _: self.pick_super_empty_dialog.pick_files(
                                    allow_multiple=False,
                                    file_type="custom",
                                    allowed_extensions=["img"],
                                ),
                                expand=True,
                            ),
                            self.selected_super_empty,
                        ]
                    ),
                    Divider(),
                ]
            )
        self.additional_image_selection.controls = additional_image_selection
        self.additional_image_selection.update()

    def open_explain_images_dlg(self, e):
        """Open the dialog to explain OS and recovery image."""
        self.page.dialog = self.dlg_explain_images
        self.dlg_explain_images.open = True
        self.page.update()

    def close_close_explain_images_dlg(self, e):
        """Close the dialog to explain OS and recovery image."""
        self.dlg_explain_images.open = False
        self.page.update()

    def open_explain_additional_images_dlg(self, e):
        """Open the dialog to explain additional images."""
        self.page.dialog = self.dlg_explain_additional_images
        self.dlg_explain_additional_images.open = True
        self.page.update()

    def close_close_explain_additional_images_dlg(self, e):
        """Close the dialog to explain additional images."""
        self.dlg_explain_additional_images.open = False
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
        # if the image works and the sdk level is 33 or higher, show the additional image selection
        if (
            self.selected_image.color == colors.GREEN
            and image_sdk_level(self.state.image_path) >= 33
        ):
            self.toggle_additional_image_selection()
        else:
            self.additional_image_selection.controls = []
            self.additional_image_selection.update()
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

    def pick_dtbo_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        if e.files:
            # check if the dtbo works with the device and show the filename in different colors accordingly
            if path == "dtbo.img":
                self.selected_dtbo.fill_color = colors.GREEN
                self.selected_dtbo.value = True
                self.state.dtbo_path = e.files[0].path
                logger.info(f"Selected dtbo from {self.state.dtbo_path}")
            else:
                self.selected_dtbo.fill_color = colors.RED
                self.selected_dtbo.value = False
        else:
            logger.info("No image selected.")
        # update
        self.selected_dtbo.update()

    def pick_vbmeta_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        if e.files:
            # check if the vbmeta works with the device and show the filename in different colors accordingly
            if path == "vbmeta.img":
                self.selected_vbmeta.fill_color = colors.GREEN
                self.selected_vbmeta.value = True
                self.state.vbmeta_path = e.files[0].path
                logger.info(f"Selected vbmeta from {self.state.vbmeta_path}")
            else:
                self.selected_vbmeta.fill_color = colors.RED
                self.selected_vbmeta.value = False
        else:
            logger.info("No image selected.")
        # update
        self.selected_vbmeta.update()

    def pick_super_empty_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # update the textfield with the name of the file
        if e.files:
            # check if the super_empty works with the device and show the filename in different colors accordingly
            if path == "super_empty.img":
                self.selected_super_empty.fill_color = colors.GREEN
                self.selected_super_empty.value = True
                self.state.super_empty_path = e.files[0].path
                logger.info(f"Selected super_empty from {self.state.super_empty_path}")
            else:
                self.selected_super_empty.fill_color = colors.RED
                self.selected_super_empty.value = False
        else:
            logger.info("No image selected.")
        # update
        self.selected_super_empty.update()

    def enable_button_if_ready(self, e):
        """Enable the confirm button if both files have been selected."""
        if (".zip" in self.selected_image.value) and (
            ".img" in self.selected_recovery.value
        ):
            if not (
                image_works_with_device(
                    supported_device_codes=self.state.config.supported_device_codes,
                    image_path=self.state.image_path,
                )
                and recovery_works_with_device(
                    supported_device_codes=self.state.config.supported_device_codes,
                    recovery_path=self.state.recovery_path,
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

            # check if the additional images work with the device
            if any(
                v == False
                for v in [
                    self.selected_dtbo.value,
                    self.selected_vbmeta.value,
                    self.selected_super_empty.value,
                ]
            ):
                logger.error(
                    "Some additional images don't match. Please select different ones."
                )
                self.info_field.controls = [
                    Text(
                        "Some additional images don't match. Please select the right ones.",
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
