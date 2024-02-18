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

from openandroidinstaller.tooling import run_command

from openandroidinstaller.tooling import adb_reboot, fastboot_flash_recovery
from openandroidinstaller.tooling import search_device


def test_adb_reboot_success(fp):
    """Test if rebooting with adb works fine."""

    with fp.context() as nested_process:
        nested_process.register(
            ["test/path/to/tools/adb", "reboot"], stdout=bytes.fromhex("00")
        )
        for line in adb_reboot(bin_path=Path("test/path/to/tools")):
            print(line)
    # for_later = "error: no devices/emulators found"
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

    assert device_code is None


def test_run_command_success(mocker):
    """Test if running a command with a tool works fine."""

    def patched_popen(*args, **kwargs):
        class MockProcess:
            stdout = [
                "Output line 1",
                "Output line 2",
                "Output line 3",
            ]
            returncode = 0

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def communicate(self):
                return self.stdout, None

        return MockProcess()

    mocker.patch("openandroidinstaller.tooling.subprocess.Popen", patched_popen)

    bin_path = Path("test/path/to/tools")
    full_command = "adb reboot"
    target = "device"
    enable_logging = True

    expected_output = [
        "$adb reboot",
        "Output line 1",
        "Output line 2",
        "Output line 3",
        True,
    ]

    output = list(
        run_command(
            full_command=full_command,
            bin_path=bin_path,
            target=target,
            enable_logging=enable_logging,
        )
    )

    assert output == expected_output


def test_run_command_failure(mocker):
    """Test if a failure in running a command with a tool is handled properly."""

    def patched_popen(*args, **kwargs):
        class MockProcess:
            stdout = [
                "Error line 1",
                "Error line 2",
                "Error line 3",
            ]
            returncode = 1

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def communicate(self):
                return self.stdout, None

        return MockProcess()

    mocker.patch("openandroidinstaller.tooling.subprocess.Popen", patched_popen)

    bin_path = Path("test/path/to/tools")
    full_command = "adb reboot"
    target = "device"
    enable_logging = True

    expected_output = [
        "$adb reboot",
        "Error line 1",
        "Error line 2",
        "Error line 3",
        False,
    ]

    output = list(
        run_command(
            full_command=full_command,
            bin_path=bin_path,
            target=target,
            enable_logging=enable_logging,
        )
    )

    assert output == expected_output


def test_run_command_unknown_tool():
    """Test if an exception is raised for an unknown tool."""

    bin_path = Path("test/path/to/tools")
    full_command = "unknown_tool command"
    target = "device"
    enable_logging = True

    try:
        list(
            run_command(
                full_command=full_command,
                bin_path=bin_path,
                target=target,
                enable_logging=enable_logging,
            )
        )
        assert False, "Exception not raised"
    except Exception as e:
        assert str(e) == "Unknown tool unknown_tool. Use adb, fastboot or heimdall."


def test_fastboot_flash_recovery_success(fp):
    """Test if flashing custom recovery with fastboot works fine."""

    def callback_function_with_kwargs(process, return_code):
        process.returncode = return_code

    return_code = 0

    with fp.context() as nested_process:
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "recovery",
                "custom_recovery.img",
            ],
            stdout=bytes.fromhex("00"),
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        for line in fastboot_flash_recovery(
            bin_path=Path("test/path/to/tools"),
            recovery="custom_recovery.img",
            is_ab=True,
        ):
            print(line)
    assert line


def test_fastboot_flash_recovery_failure(fp):
    """Test if a failure in flashing custom recovery with fastboot is handled properly."""

    def callback_function_with_kwargs(process, return_code):
        process.returncode = return_code

    return_code = 1

    with fp.context() as nested_process:
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "recovery",
                "custom_recovery.img",
            ],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        for line in fastboot_flash_recovery(
            bin_path=Path("test/path/to/tools"),
            recovery="custom_recovery.img",
            is_ab=True,
        ):
            print(line)
    assert not line


def test_fastboot_flash_recovery_with_additional_partitions_success(fp):
    """Test if flashing custom recovery with additional partitions using fastboot works fine."""

    def callback_function_with_kwargs(process, return_code):
        process.returncode = return_code

    return_code = 0

    with fp.context() as nested_process:
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "dtbo",
                "dtbo.img",
            ],
            stdout=bytes.fromhex("00"),
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "--disable-verity",
                "--disable-verification",
                "flash",
                "vbmeta",
                "vbmeta.img",
            ],
            stdout=bytes.fromhex("00"),
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "wipe-super",
                "super_empty.img",
            ],
            stdout=bytes.fromhex("00"),
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "vendor_boot",
                "vendor_boot.img",
            ],
            stdout=bytes.fromhex("00"),
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "recovery",
                "custom_recovery.img",
            ],
            stdout=bytes.fromhex("00"),
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        for line in fastboot_flash_recovery(
            bin_path=Path("test/path/to/tools"),
            recovery="custom_recovery.img",
            is_ab=True,
            vendor_boot="vendor_boot.img",
            dtbo="dtbo.img",
            vbmeta="vbmeta.img",
            super_empty="super_empty.img",
        ):
            print(line)
    assert line


def test_fastboot_flash_recovery_with_additional_partitions_failure(fp):
    """Test if a failure in flashing custom recovery with additional partitions using fastboot is handled properly."""

    def callback_function_with_kwargs(process, return_code):
        process.returncode = return_code

    return_code = 1

    with fp.context() as nested_process:
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "dtbo",
                "dtbo.img",
            ],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "--disable-verity",
                "--disable-verification",
                "flash",
                "vbmeta",
                "vbmeta.img",
            ],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "wipe-super",
                "super_empty.img",
            ],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "vendor_boot",
                "vendor_boot.img",
            ],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        nested_process.register(
            [
                "test/path/to/tools/fastboot",
                "flash",
                "recovery",
                "custom_recovery.img",
            ],
            stdout=[
                bytes("error: no devices/emulators found", encoding="utf-8"),
            ],
            callback=callback_function_with_kwargs,
            callback_kwargs={"return_code": return_code},
        )
        for line in fastboot_flash_recovery(
            bin_path=Path("test/path/to/tools"),
            recovery="custom_recovery.img",
            is_ab=True,
            vendor_boot="vendor_boot.img",
            dtbo="dtbo.img",
            vbmeta="vbmeta.img",
            super_empty="super_empty.img",
        ):
            print(line)
    assert not line
