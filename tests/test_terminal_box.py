"""Test the TerminalBox class."""

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

import pytest
from flet import Container, Page

from openandroidinstaller.views.step_view import TerminalBox


def test_init_box():
    """Test if the box can be initialized properly."""
    terminal_box = TerminalBox(expand=True)
    build_box = terminal_box.build()

    assert isinstance(build_box, Container)


def test_write_lines(mocker):
    """Test if we can write lines to the terminal and bools are ignored."""
    mocker.patch(
        "openandroidinstaller.views.step_view.TerminalBox.update",
        return_value=True,
        new_callable=mocker.Mock,
    )

    terminal_box = TerminalBox(expand=True)
    _ = terminal_box.build()

    # write some lines
    for line in ["test", "test_line2", True]:
        terminal_box.write_line(line)

    # two text elements should appear
    assert len(terminal_box._box.content.controls) == 2


def test_toggle_visibility(mocker):
    """Test if the visibility toggle method works."""
    mocker.patch(
        "openandroidinstaller.views.step_view.TerminalBox.update",
        return_value=True,
        new_callable=mocker.Mock,
    )

    terminal_box = TerminalBox(expand=True)
    _ = terminal_box.build()

    # should be non-visible at the beginning
    assert terminal_box._box.visible == False
    # now toggle
    terminal_box.toggle_visibility()
    # now should be visible
    assert terminal_box._box.visible == True
    # now toggle again
    terminal_box.toggle_visibility()
    # now it should be non-visible again
    assert terminal_box._box.visible == False


def test_clear_terminal(mocker):
    """Test if the terminal can be cleared properly."""
    mocker.patch(
        "openandroidinstaller.views.step_view.TerminalBox.update",
        return_value=True,
        new_callable=mocker.Mock,
    )

    terminal_box = TerminalBox(expand=True)
    _ = terminal_box.build()

    # write some lines
    for line in ["test", "test_line2", True]:
        terminal_box.write_line(line)

    # now clear
    terminal_box.clear()

    # two text elements should appear
    assert len(terminal_box._box.content.controls) == 0
