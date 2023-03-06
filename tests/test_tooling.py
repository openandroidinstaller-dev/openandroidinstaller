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

from openandroidinstaller.tooling import (
    adb_reboot,
    search_device,
    check_ab_partition,
)


def test_adb_reboot_success(fp):
    """Test if rebooting with adb works fine."""

    with fp.context() as nested_process:
        nested_process.register(
            ["test/path/to/tools/adb", "reboot"], stdout=bytes.fromhex("00")
        )
        for line in adb_reboot(bin_path=Path("test/path/to/tools")):
            print(line)
    for_later = "error: no devices/emulators found"
    assert line


def test_adb_reboot_failure(fp):
    """Test if a fail in rebooting with adb is handled properly."""

    def callback_function_with_kwargs(process, return_code):
        process.returncode = return_code

    return_code = 1

    with fp.context() as nested_process:
        nested_process.register(
            ["test/path/to/tools/adb", "reboot"],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        for line in adb_reboot(bin_path=Path("test/path/to/tools")):
            print(line)
    assert not line


def test_search_device_success(mocker):
    """Test if search works fine."""
    mocker.patch(
        "openandroidinstaller.tooling.check_output",
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
        "openandroidinstaller.tooling.check_output",
        patched_check_output,
    )

    device_code = search_device(
        platform="linux", bin_path=Path("openandroidinstaller/bin/")
    )

    assert device_code == None


def test_check_ab_device_is_ab(mocker):
    """Test if checking for ab device works fine."""
    mocker.patch(
        "openandroidinstaller.tooling.check_output",
        return_value=b"[ro.boot.slot_suffix]: [_b]",
    )

    # test linux
    is_ab = check_ab_partition(
        platform="linux", bin_path=Path("openandroidinstaller/bin/")
    )

    assert is_ab

    # test windows
    is_ab = check_ab_partition(
        platform="windows", bin_path=Path("openandroidinstaller/bin/")
    )

    assert is_ab


def test_check_ab_device_not_ab(mocker):
    """Test if checking for ab device returns False if it fails."""

    def patched_check_output(*args, **kwargs):
        raise CalledProcessError(returncode=1, cmd="output is None")

    mocker.patch(
        "openandroidinstaller.tooling.check_output",
        patched_check_output,
    )

    is_ab = check_ab_partition(
        platform="linux", bin_path=Path("openandroidinstaller/bin/")
    )

    assert not is_ab
