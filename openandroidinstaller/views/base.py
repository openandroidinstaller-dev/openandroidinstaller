"""Contains the base class for views."""

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

from flet import (
    Column,
    Image,
    Row,
    UserControl,
    VerticalDivider,
)


class BaseView(UserControl):
    def __init__(self, state: AppState, image: str = "placeholder.png"):
        super().__init__()
        self.state = state

        # configs
        self.column_width = 600
        # right part of the display, add content here.
        self.right_view_header = Column(width=self.column_width, height=100, spacing=30)
        self.right_view = Column(
            alignment="center", width=self.column_width, height=650
        )
        # left part of the display: used for displaying the images
        self.left_view = Column(
            width=self.column_width,
            controls=[Image(src=f"/assets/imgs/{image}", height=600)],
            expand=True,
            horizontal_alignment="center",
        )
        # main view row
        self.view = Row(
            [
                self.left_view,
                VerticalDivider(),
                Column(expand=True, controls=[self.right_view_header, self.right_view]),
            ],
            alignment="spaceEvenly",
        )

    def clear(
        self,
    ):
        """Clear the right view."""
        self.right_view.controls = []
        self.right_view_header.controls = []
