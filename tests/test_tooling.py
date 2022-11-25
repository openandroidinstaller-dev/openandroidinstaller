"""Test interactions with tools like adb and fastboot"""

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

from pathlib import Path
from subprocess import CalledProcessError

from tooling import search_device


def test_search_device_success(mocker):
    """Test if search works fine."""
    mocker.patch(
        "openandroidinstaller.tool_utils.check_output",
        return_value=b"[ro.product.device]: [sargo]",
    )

    # test linux
    device_code = search_device(
        platform="linux", bin_path=Path("openandroidinstaller/bin/")
    )

    assert device_code == "sargo"

    # test windows
    device_code = search_device(
        platform="windows", bin_path=Path("openandroidinstaller/bin/")
    )

    assert device_code == "sargo"


def test_search_device_failure(mocker):
    """Test if search failure is escalated properly."""

    def patched_check_output(*args, **kwargs):
        raise CalledProcessError(returncode=1, cmd="search device failed")

    mocker.patch(
        "openandroidinstaller.tool_utils.check_output",
        patched_check_output,
    )

    device_code = search_device(
        platform="linux", bin_path=Path("openandroidinstaller/bin/")
    )

    assert device_code == None
