"""Test the ProgressIndicator class."""

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
from flet import Container

from openandroidinstaller.widgets import ProgressIndicator


def test_init():
    """Test if the field can be initialized properly."""
    progress_indicator = ProgressIndicator(expand=True)
    build_indicator = progress_indicator.build()

    assert isinstance(build_indicator, Container)


def test_update_progress_bar():
    """Test if the progress bar is updated properly based on lines."""
    progress_indicator = ProgressIndicator(expand=True)
    progress_indicator.build()

    # test if other line is fine
    progress_indicator.display_progress_bar(
        line="Failed to mount '/data' (Device or resource busy)"
    )
    assert progress_indicator.progress_bar

    # test if percentages are parsed correctly and update is performed
    for percentage in range(1, 47):
        line = f"serving: '/home/tobias/Repositories/openandroidinstaller/images/google-pixel3a/lineage-19.1-20221004-nightly-sargo-signed.zip'  (~{percentage}%)\n"
        progress_indicator.display_progress_bar(line)
        assert progress_indicator.progress_bar.value == percentage / 100

    # test if the finishing print is detected and updated correctly.
    progress_indicator.display_progress_bar(line="Total xfer: 1.00x\n")
    assert progress_indicator.progress_bar.value == 0.99

    # test if the final set_progress_bar is working correctly
    progress_indicator.set_progress_bar(100)
    assert progress_indicator.progress_bar.value == 1.0
