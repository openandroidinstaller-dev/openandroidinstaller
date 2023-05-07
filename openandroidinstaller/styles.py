"""This module contains different pre-configured style elements for building the application."""

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

import flet as ft


class Text(ft.Text):
    """Text element to replace the default text element from flet but is selectable."""

    def __init__(self, *args, **kwargs):
        super().__init__(selectable=True, *args, **kwargs)


class Markdown(ft.Markdown):
    """Markdown element to replace the markdown element from flet but is selectable."""

    def __init__(self, *args, **kwargs):
        super().__init__(selectable=True, auto_follow_links=True, *args, **kwargs)
