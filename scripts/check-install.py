"""Check if adb works and print the version."""

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

from subprocess import STDOUT, check_output


def check_adb_version():
    return check_output(["adb", "version"], stderr=STDOUT).decode()


if __name__ == "__main__":
    print("Checking if adb is installed...")
    adb_version = check_adb_version()
    if adb_version:
        print(adb_version)
        print("Done.")
    else:
        print("Failed.")
