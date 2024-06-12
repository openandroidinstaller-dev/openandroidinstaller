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
    colors,
    icons,
)
from flet_core.buttons import ContinuousRectangleBorder
from loguru import logger
from translations import _
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
            title=Text(_("supported_addons_title")),
            content=Markdown(
                _("supported_addons_text"),
            ),
            actions=[
                TextButton(_("close"), on_click=self.close_close_explain_addons_dlg),
            ],
            actions_alignment="end",
            shape=ContinuousRectangleBorder(radius=0),
        )

        # initialize file pickers
        self.pick_addons_dialog = FilePicker(on_result=self.pick_addons_result)
        self.selected_addons = Text(_("selected_addons"))

        # initialize and manage button state.
        # wrap the call to the next step in a call to boot fastboot

        self.confirm_button = confirm_button(self.on_confirm)
        # self.confirm_button.disabled = True
        # self.pick_addons_dialog.on_result = self.enable_button_if_ready

        # attach hidden dialogues
        self.right_view.controls.append(self.pick_addons_dialog)

        # create help/info button to show the help dialog
        info_button = OutlinedButton(
            _("supported_addons_title"),
            on_click=self.open_explain_addons_dlg,
            expand=True,
            icon=icons.HELP_OUTLINE_OUTLINED,
            icon_color=colors.DEEP_ORANGE_500,
            tooltip=_("supported_addons_tooltip"),
        )

        # add title
        self.right_view_header.controls.append(
            get_title(
                _("select_additional_addons"),
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
                    Text(_("download_fdroid_text")),
                    Row(
                        [
                            ElevatedButton(
                                _("download_fdroid"),
                                icon=icons.DOWNLOAD_OUTLINED,
                                on_click=lambda _: webbrowser.open(
                                    "https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota/"
                                ),
                                expand=True,
                            ),
                        ]
                    ),
                    Text(_("download_gapps_text")),
                    Row(
                        [
                            ElevatedButton(
                                _("download_gapps"),
                                icon=icons.DOWNLOAD_OUTLINED,
                                on_click=lambda _: webbrowser.open(
                                    "https://wiki.lineageos.org/gapps#downloads"
                                ),
                                expand=True,
                            ),
                        ]
                    ),
                    Text(_("download_microg_text")),
                    Row(
                        [
                            ElevatedButton(
                                _("download_microg"),
                                icon=icons.DOWNLOAD_OUTLINED,
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
                # Markdown(
                # f"""
                # The image file should look something like `lineage-20.0-20240101-nightly-{self.state.config.metadata.get('devicecode')}-signed.zip`."""
                #                ),
                Row(
                    [
                        FilledButton(
                            _("pick_addons"),
                            icon=icons.UPLOAD_FILE,
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

    def open_explain_addons_dlg(self, e):
        """Open the dialog to explain addons."""
        self.page.dialog = self.dlg_explain_addons
        self.dlg_explain_addons.open = True
        self.page.update()

    def close_close_explain_addons_dlg(self, e):
        """Close the dialog to explain addons."""
        self.dlg_explain_addons.open = False
        self.page.update()

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
