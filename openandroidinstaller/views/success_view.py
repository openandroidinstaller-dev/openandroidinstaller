"""Contains the final success view."""

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
from app_state import AppState
from flet import ElevatedButton, Row
from loguru import logger
from translations import _
from styles import Markdown, Text
from views import BaseView
from widgets import get_title


class SuccessView(BaseView):
    def __init__(self, state: AppState):
        super().__init__(state=state, image="success.png")

    def build(
        self,
    ):
        def close_window(e):
            logger.success("Success! Close the window.")
            # close the window
            self.page.window_close()

        # right view header
        self.right_view_header.controls = [
            get_title(_("installation_complete_title")),
        ]
        # right view main part
        contribute_link = "https://openandroidinstaller.org/#contribute"
        self.right_view.controls = [
            Text(
                _("device_boot_have_fun"),
                style="titleSmall",
            ),
            Markdown(
                _("spread_the_word {link}").format(link=contribute_link),
            ),
            Row(
                [
                    ElevatedButton(
                        _("finish_close"),
                        expand=True,
                        on_click=close_window,
                    )
                ]
            ),
        ]
        return self.view
