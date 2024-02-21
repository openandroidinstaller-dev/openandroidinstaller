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
from styles import Markdown, Text
from views import BaseView
from widgets import get_title
from translations import _


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
            get_title(_("Installation completed successfully!")),
        ]
        # right view main part
        contribute_link = "https://openandroidinstaller.org/#contribute"
        self.right_view.controls = [
            Text(
                _("Now your devices boots into the new OS. Have fun with it!"),
                style="titleSmall",
            ),
            Markdown(
                _("""
If you liked the tool, help spread the word and **share it with people** who might want to use it.

Also, you can consider contributing to make it better. There are a lot of different ways how you can help!

[How to contribute]({contribute_link})
""").format(contribute_link=contribute_link),
            ),
            Row(
                [
                    ElevatedButton(
                        "Finish and close",
                        expand=True,
                        on_click=close_window,
                    )
                ]
            ),
        ]
        return self.view
