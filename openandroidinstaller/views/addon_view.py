"""Contains the select addons view."""

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
from typing import Callable

from app_state import AppState
from flet import (
    AlertDialog,
    Column,
    Divider,
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    FilledButton,
    OutlinedButton,
    Row,
    TextButton,
    Colors,
    Icons,
    ContinuousRectangleBorder,
)
from loguru import logger
from styles import Markdown, Text
from views import BaseView
from widgets import confirm_button, get_title


class AddonsView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state)
        self.on_confirm = on_confirm

    def build(self):
        # dialog box to explain OS images and recovery
        self.dlg_explain_addons = AlertDialog(
            modal=True,
            title=Text("What kind of addons are supported?"),
            content=Markdown(
                """Please select all addons you want to install at once. See for the most common ones below.

## Google Apps & Services:
The packages listed here will bring back Google functionality to your phone, required by many proprietary apps.

### Full sets
The most known packages, including apps and services, are:

- **[MindTheGapps](https://wiki.lineageos.org/gapps/)** ([Download](https://wiki.lineageos.org/gapps/#downloads)):
  Proprietary **Google-branded applications that come pre-installed** with most Android devices, such as the Play Store, Gmail, Maps, etc.
- **[NikGApps](https://nikgapps.com)** ([Download](https://sourceforge.net/projects/nikgapps/files/Releases/)):
  choose your **set of Google Apps** and have NikGApps manage them more sustainable

### Only services
The most known packages, giving you google functionality but no google apps, are:

- **[MicroG](https://github.com/microg/GmsCore/wiki)** ([Download](https://github.com/microg/GmsCore/wiki/Installation)):
  **free-as-in-freedom re-implementation of Google**'s proprietary Android user space libraries and functionality (installable after custom ROM installation as APK but might have problems with spoofing)

These are dependend on the version of your **Android OS version** (Stock ROM) and the **phone's architecture**. You can find that information most likely on [LineageOS' device page](https://wiki.lineageos.org/devices).

If you got that, get your file from the above link like this (you can **only use one** at a time):

- `MindTheGapps-<AndroidVersion>-<architecture>-<date>_<time>.zip` (with Android 12L being 12.1)
- `NikGapps-<flavour>-<architecture>-<AndroidVersion>-<date>-signed.zip` (with [flavours](https://nikgapps.com/downloads) from minimal Google support (`core`) to full experience (`full`))
- MircoG has only one zip

## F-Droid Appstore

F-Droid is an installable **catalogue of libre software apps** for Android. The F-Droid client app makes it easy to browse, install, and keep track of updates on your device, just like the Google Play Store.

Recommended **installation** is to use the zip from here:
[https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota](https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota).
""",
            ),
            actions=[
                TextButton(
                    "Close", on_click=lambda _: self.page.close(self.dlg_explain_addons)
                ),
            ],
            actions_alignment="end",
            shape=ContinuousRectangleBorder(radius=0),
        )

        # initialize file pickers
        self.pick_addons_dialog = FilePicker(on_result=self.pick_addons_result)
        self.selected_addons = Text("Selected addons: ")

        # initialize and manage button state.
        # wrap the call to the next step in a call to boot fastboot

        self.confirm_button = confirm_button(self.on_confirm)
        # self.confirm_button.disabled = True
        # self.pick_addons_dialog.on_result = self.enable_button_if_ready

        # attach hidden dialogues
        self.right_view.controls.append(self.pick_addons_dialog)

        # create help/info button to show the help dialog
        info_button = OutlinedButton(
            "What kind of addons?",
            on_click=lambda _: self.page.open(self.dlg_explain_addons),
            expand=True,
            icon=Icons.HELP_OUTLINE_OUTLINED,
            icon_color=Colors.DEEP_ORANGE_500,
            tooltip="Get more details on what addons are supported.",
        )

        # add title
        self.right_view_header.controls.append(
            get_title(
                "You can select additional addons to install.",
                info_button=info_button,
                step_indicator_img="steps-header-select.png",
            )
        )

        # text row to show infos during the process
        self.info_field = Row()
        # if there is an available download, show the button to the page
        self.right_view.controls.append(Divider())
        self.right_view.controls.append(
            Column(
                [
                    Text("Here you can download the F-Droid App-Store:"),
                    Row(
                        [
                            ElevatedButton(
                                "Download F-Droid App-Store",
                                icon=Icons.DOWNLOAD_OUTLINED,
                                on_click=lambda _: webbrowser.open(
                                    "https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota/"
                                ),
                                expand=True,
                            ),
                        ]
                    ),
                    Text(
                        "Here you can find instructions on how to download the right Google apps for your device."
                    ),
                    Row(
                        [
                            ElevatedButton(
                                "Download Google Apps",
                                icon=Icons.DOWNLOAD_OUTLINED,
                                on_click=lambda _: webbrowser.open(
                                    "https://wiki.lineageos.org/gapps#downloads"
                                ),
                                expand=True,
                            ),
                        ]
                    ),
                    Text("Here you can download MicroG:"),
                    Row(
                        [
                            ElevatedButton(
                                "Download MicroG",
                                icon=Icons.DOWNLOAD_OUTLINED,
                                on_click=lambda _: webbrowser.open(
                                    "https://github.com/FriendlyNeighborhoodShane/MinMicroG-abuse-CI/releases"
                                ),
                                expand=True,
                            ),
                        ]
                    ),
                    Divider(),
                ]
            )
        )
        # attach the controls for uploading addons
        self.right_view.controls.extend(
            [
                Text("Select addons:", style="titleSmall"),
                Row(
                    [
                        FilledButton(
                            "Pick the addons you want to install",
                            icon=Icons.UPLOAD_FILE,
                            on_click=lambda _: self.pick_addons_dialog.pick_files(
                                allow_multiple=True,
                                file_type="custom",
                                allowed_extensions=["zip"],
                            ),
                            expand=True,
                        ),
                    ]
                ),
                self.selected_addons,
                Divider(),
                self.info_field,
                Row([self.confirm_button]),
            ]
        )
        return self.view

    def pick_addons_result(self, e: FilePickerResultEvent):
        path = ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        # update the textfield with the name of the file
        self.selected_addons.value = (
            self.selected_addons.value.split(":")[0] + f": {path}"
        )
        if e.files:
            self.addon_paths = [file.path for file in e.files]
            self.state.addon_paths = self.addon_paths
            logger.info(f"Selected addons: {self.addon_paths}")
        else:
            logger.info("No addons selected.")
        # check if the addons works with the device and show the filename in different colors accordingly
        # update
        self.selected_addons.update()
