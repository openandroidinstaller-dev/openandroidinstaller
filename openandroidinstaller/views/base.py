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
from loguru import logger

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
        # right part of the display, add content here.
        self.right_view = Column(expand=True)
        # left part of the display: used for displaying the images
        self.left_view = Column(
            width=600,
            controls=[Image(src=f"/assets/imgs/{image}")],
            expand=True,
            horizontal_alignment="center",
        )
        # main view row
        self.view = Row(
            [self.left_view, VerticalDivider(), self.right_view],
            alignment="spaceEvenly",
        )