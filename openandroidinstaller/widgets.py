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
import webbrowser
from functools import partial
from typing import Callable, Optional

import regex as re
from flet import (
    Column,
    Container,
    ElevatedButton,
    IconButton,
    Image,
    ProgressBar,
    ProgressRing,
    Row,
    UserControl,
    alignment,
    colors,
    icons,
)
from styles import Text


class TerminalBox(UserControl):
    def __init__(self, expand: bool = True, visible: bool = False):
        super().__init__(expand=expand)
        self.visible = visible

    def build(self):
        self._box = Container(
            content=Column(
                controls=[Text("")],
                scroll="auto",
                expand=True,
                auto_scroll=True,
            ),
            margin=10,
            padding=10,
            alignment=alignment.top_left,
            bgcolor=colors.BLACK38,
            height=300,
            border_radius=2,
            expand=True,
            visible=self.visible,
        )
        return self._box

    def write_line(self, line: str):
        """
        Write the line to the window box and update.

        Ignores empty lines.
        """
        if isinstance(line, str) and line.strip():
            self._box.content.controls[0].value += f"\n>{line.strip()}"
            self._box.content.controls[0].value = self._box.content.controls[
                0
            ].value.strip("\n")
            self.update()

    def toggle_visibility(self):
        """Toggle the visibility of the terminal box."""
        self._box.visible = not self._box.visible
        self.visible = not self.visible
        self.update()

    def clear(self):
        """Clear terminal output."""
        self._box.content.controls[0].value = ""
        self.update()

    def update(self):
        """Update the view."""
        self._box.update()


class ProgressIndicator(UserControl):
    def __init__(self, expand: bool = True):
        super().__init__(expand=expand)
        # placeholder for the flashing progressbar
        self.progress_bar = None
        # progress ring to display
        self.progress_ring = None

    def build(self):
        self._container = Container(
            content=Column(scroll="auto", expand=True),
            margin=10,
            alignment=alignment.center,
            height=50,
            expand=True,
            visible=True,
        )
        return self._container

    def display_progress_bar(self, line: str):
        """Display and update the progress bar for the given line."""
        percentage_done = None
        result = None
        # create the progress bar
        if not self.progress_bar:
            self.progress_bar = ProgressBar(
                value=1 / 100,
                width=500,
                bar_height=32,
                color="#00d886",
                bgcolor="#eeeeee",
            )
            # text to display the percentage
            self.percentage_text = Text("1%")
            self._container.content.controls.append(
                Row([self.percentage_text, self.progress_bar])
            )
        # get the progress numbers from the output lines
        if isinstance(line, str) and line.strip():
            result = re.search(
                r"\(\~(\d{1,3})\%\)|(Total xfer:|adb: failed to read command: Success)",
                line.strip(),
            )
        if result:
            if result.group(2):
                percentage_done = 99
            elif result.group(1):
                percentage_done = int(result.group(1))
                percentage_done = max(1, min(99, percentage_done))
            # update the progress bar
            self.set_progress_bar(percentage_done)

    def set_progress_bar(self, percentage_done: int):
        """Set the progress bar to the given percentage.

        Args:
            percentage_done (int): Percentage of the progress bar to be filled.
        """
        assert percentage_done >= 0, "Percentage must be non-negative."
        # clip the percentage to 100
        if percentage_done > 100:
            percentage_done = 100
        if self.progress_bar:
            self.progress_bar.value = percentage_done / 100
            self.percentage_text.value = f"{percentage_done}%"

    def display_progress_ring(
        self,
    ):
        """Display a progress ring to signal progress."""
        if not self.progress_ring:
            self.progress_ring = ProgressRing(color="#00d886")
            self._container.content.controls.append(self.progress_ring)
            self._container.update()

    def clear(self):
        """Clear output."""
        self._container.content.controls = []
        self.progress_ring = None
        self.progress_bar = None
        self.update()

    def update(self):
        """Update the view."""
        self._container.update()


def get_title(
    title: str, info_button: IconButton = None, step_indicator_img: Optional[str] = None
) -> Container:
    """Function to get the title header element for the right side view."""
    if info_button:
        content = Row([Text(f"{title}", style="titleLarge"), info_button])
    else:
        content = Row([Text(f"{title}", style="titleLarge")])
    if step_indicator_img:
        content = Column(
            controls=[
                Image(
                    src=f"/imgs/{step_indicator_img}",
                    fit="fitWidth",
                    tooltip=f"Current step: {title}",
                    width=600,
                ),
                content,
            ]
        )
    return Container(
        content=content,
        margin=0,
        padding=0,
        alignment=alignment.center,
        width=600,
        height=150,
        border_radius=1,
    )


def confirm_button(
    confirm_func: Callable, confirm_text: str = "Continue"
) -> ElevatedButton:
    """Get a button, that calls a given function when clicked."""
    return ElevatedButton(
        f"{confirm_text}",
        on_click=confirm_func,
        icon=icons.NEXT_PLAN_OUTLINED,
        expand=True,
    )


def call_button(
    call_func: Callable, command: str, confirm_text: str = "Confirm and run"
) -> ElevatedButton:
    """Get a button, that calls a given function with given command when clicked."""
    return ElevatedButton(
        f"{confirm_text}",
        on_click=partial(call_func, command=command),
        expand=True,
        icon=icons.DIRECTIONS_RUN_OUTLINED,
    )


def link_button(link: str, text: str) -> ElevatedButton:
    """Get a button that opens a link in a browser."""
    return ElevatedButton(
        f"{text}",
        on_click=lambda _: webbrowser.open(link),
        expand=True,
    )
