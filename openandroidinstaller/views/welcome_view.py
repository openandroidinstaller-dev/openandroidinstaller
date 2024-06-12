"""Contains the welcome view."""

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
from typing import Callable

from app_state import AppState
from flet import Divider, ElevatedButton, Row, icons
from styles import Markdown, Text
from views import BaseView
from widgets import get_title
from translations import _


class WelcomeView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state, image="connect-to-usb.png")
        self.on_confirm = on_confirm

        self.init_visuals()

    def init_visuals(
        self,
    ):
        """Initialize the stateful visual elements of the view."""
        self.continue_button = ElevatedButton(
            _("lets_start"),
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=False,
            expand=True,
        )

    def build(self):
        self.clear()

        # build up the main view
        self.right_view_header.controls.extend(
            [get_title(_("welcome_title"))]
        )
        self.right_view.controls.extend(
            [
                Text(
                    _("great_install_alternative")
                ),
                Text(
                    _("nice_and_easy")
                ),
                Markdown(
                    _("what_will_be_done_text")
                ),
                Divider(),
                Markdown(
                    _("prerequisites_text")
                ),
                Divider(),
                Row(
                    [
                        self.continue_button,
                    ],
                    alignment="center",
                ),
            ]
        )
        return self.view
