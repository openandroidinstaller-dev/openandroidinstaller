"""Contains the start view."""

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
    FilledButton,
    OutlinedButton,
    ResponsiveRow,
    Row,
    Switch,
    TextButton,
    colors,
    icons,
)
from flet_core.buttons import ContinuousRectangleBorder
from loguru import logger
from translations import _
from styles import Markdown, Text
from tooling import search_device, SearchResult
from views import BaseView
from widgets import get_title


class StartView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
        on_back: Callable,
    ):
        super().__init__(state=state, image="connect-to-usb.png")
        self.on_confirm = on_confirm
        self.on_back = on_back

        self.init_visuals()

    def init_visuals(
        self,
    ):
        """Initialize the stateful visual elements of the view."""
        self.continue_button = ElevatedButton(
            _("continue"),
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=True,
            expand=True,
        )
        self.back_button = ElevatedButton(
            _("back"),
            on_click=self.on_back,
            icon=icons.ARROW_BACK,
            expand=True,
        )

        # dialog box to help with developer options
        self.dlg_help_developer_options = AlertDialog(
            modal=True,
            title=Text(_("how_to_developer_oem_title")),
            content=Markdown(
                _("how_to_developer_oem_text")
            ),
            actions=[
                TextButton(_("close"), on_click=self.close_developer_options_dlg),
            ],
            actions_alignment="end",
            shape=ContinuousRectangleBorder(radius=0),
        )

        # toggleswitch to allow skipping unlocking the bootloader
        def check_bootloader_unlocked(e):
            """Enable skipping unlocking the bootloader if selected."""
            self.state.toggle_flash_unlock_bootloader()

        self.bootloader_switch = Switch(
            label=_("bootloader_already_unlock"),
            on_change=check_bootloader_unlocked,
            disabled=True,
            inactive_thumb_color=colors.YELLOW,
            active_color=colors.GREEN,
            col={"xl": 6},
        )

        # toggleswitch to allow skipping flashing recovery
        def check_recovery_already_flashed(e):
            """Enable skipping flashing recovery if selected."""
            self.state.toggle_flash_recovery()

        self.recovery_switch = Switch(
            label=_("recovery_already_flashed"),
            on_change=check_recovery_already_flashed,
            disabled=True,
            inactive_thumb_color=colors.YELLOW,
            active_color=colors.GREEN,
            col={"xl": 6},
        )

        # inform the user about the device detection
        self.device_name = Text("", weight="bold")
        self.device_detection_infobox = Row(
            [Text(_("detected_device")), self.device_name]
        )
        self.device_request_row = Row([], alignment="center")
        self.device_infobox = Column(
            [
                self.device_detection_infobox,
                self.device_request_row,
            ]
        )

    def build(self):
        self.clear()

        # build up the main view
        self.right_view_header.controls.extend(
            [
                get_title(
                    _("get_phone_ready_title"),
                    step_indicator_img="steps-header-get-ready.png",
                )
            ]
        )
        self.right_view.controls.extend(
            [
                Markdown(_("get_phone_ready_text")),
                Row(
                    [
                        OutlinedButton(
                            _("how_to_developer"),
                            on_click=self.open_developer_options_dlg,
                            expand=True,
                            icon=icons.HELP_OUTLINE_OUTLINED,
                            icon_color=colors.DEEP_ORANGE_500,
                            tooltip=_("how_to_developer_oem_tooltip"),
                        )
                    ]
                ),
                Divider(),
                Markdown(_("how_to_developer_text")),
                Divider(),
                Markdown(
                    _("toggle_already_bootloader_recovery_text")
                ),
                self.device_infobox,
                Row(
                    [
                        self.back_button,
                        FilledButton(
                            _("search_device"),
                            on_click=self.search_devices_clicked,
                            icon=icons.DEVICES_OTHER_OUTLINED,
                            expand=True,
                            tooltip=_("search_device_tooltip"),
                        ),
                        self.continue_button,
                    ],
                    alignment="center",
                ),
                Divider(),
                ResponsiveRow([self.bootloader_switch, self.recovery_switch]),
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

    def search_devices_clicked(self, e):
        """Search the device when the button is clicked."""
        self.device_request_row.controls.clear()
        # search the device
        if self.state.test:
            # this only happens for testing
            result = SearchResult(
                device_code=self.state.test_config,
                msg=_("device_found {code}").format(code=self.state.test_config),
            )
            logger.info(
                f"Running search in development mode and loading config {result.device_code}.yaml."
            )
        else:
            result = search_device(
                platform=self.state.platform, bin_path=self.state.bin_path
            )
            if result.device_code:
                self.device_name.value = result.device_code
                self.device_name.color = colors.BLACK
            else:
                logger.info("No device detected! Connect to USB and try again.")
                self.device_name.value = result.msg
                self.device_name.color = colors.RED

        # load the config, if a device is detected
        if result.device_code:
            self.device_name.value = result.device_code
            # load config from file
            self.state.load_config(result.device_code)
            if self.state.config:
                device_name = self.state.config.metadata.get(
                    "device_name", "No device name in config."
                )
            else:
                device_name = None

            # display success in the application
            if device_name:
                self.continue_button.disabled = False
                self.bootloader_switch.disabled = False
                self.recovery_switch.disabled = False
                # overwrite the text field with the real name from the config
                self.device_name.value = (
                    f"{device_name} (code: {self.state.config.device_code})"
                )
                self.device_name.color = colors.GREEN
                # if there are no steps for bootloader unlocking, assume there is nothing to do and toggle the switch
                if len(self.state.config.unlock_bootloader) == 0:
                    self.bootloader_switch.value = True
            else:
                # failed to load config or device is not supported
                logger.error(
                    f"Device with code '{result.device_code}' is not supported or the config is corrupted. Please check the logs for more information."
                )
                self.device_name.value = (
                    _("device_unsupported {device}").format(device=result.device_code)
                )
                # add request support for device button
                request_url = f"https://github.com/openandroidinstaller-dev/openandroidinstaller/issues/new?labels=device&template=device-support-request.yaml&title=Add support for `{result.device_code}`"
                self.device_request_row.controls.append(
                    ElevatedButton(
                        _("request_support"),
                        icon=icons.PHONELINK_SETUP_OUTLINED,
                        on_click=lambda _: webbrowser.open(request_url),
                    )
                )
                self.device_name.color = colors.RED
        self.view.update()
