"""Contains functions and classes to get different elements and widgets of the installer."""

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

from functools import partial
from os import path
from typing import Callable

from flet import Column, Container, ElevatedButton, Image, Row, Text, alignment, icons


def get_title(title: str):
    image_path = path.abspath(
        path.join(path.dirname(__file__), "assets/logo-192x192.png")
    )
    return Container(
        content=Row(
            [
                Text(f"{title}", style="titleMedium"),
            ]
        ),
        margin=0,
        padding=0,
        alignment=alignment.center,
        width=400,
        height=50,
        border_radius=1,
    )


def confirm_button(
    text: str, confirm_func: Callable, confirm_text: str = "Confirm and continue"
) -> Column:
    return Column(
        [
            Text(f"{text}"),
            Row(
                [
                    ElevatedButton(
                        f"{confirm_text}",
                        on_click=confirm_func,
                        icon=icons.NEXT_PLAN_OUTLINED,
                        expand=True,
                    )
                ]
            ),
        ],
        horizontal_alignment="center",
    )


def call_button(
    text: str, call_func: Callable, command: str, confirm_text: str = "Confirm and run"
) -> Column:
    return Column(
        [
            Text(f"{text}"),
            Row(
                [
                    ElevatedButton(
                        f"{confirm_text}",
                        on_click=partial(call_func, command=command),
                        expand=True,
                        icon=icons.DIRECTIONS_RUN_OUTLINED,
                    )
                ]
            ),
        ],
        horizontal_alignment="center",
    )
