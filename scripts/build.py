"""Script to build the OpenAndroidInstaller executable on different platforms with pyinstaller."""

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

import subprocess
import sys

from loguru import logger

added_files = [
    ("openandroidinstaller/assets", "assets"),
    ("openandroidinstaller/bin", "bin"),
]


def build_linux():
    added_data = [f"--add-data={src}:{dst}" for src, dst in added_files]
    pyinstaller_options = [
        "--onefile",
        "--noconsole",
        "--noconfirm",
        "--windowed",
        "--clean",
        "--icon=openandroidinstaller/assets/favicon.ico",
        "--paths=openandroidinstaller",
    ] + added_data

    logger.info(f"Running pyinstaller with: {' '.join(pyinstaller_options)}")
    res = subprocess.call(
        ["pyinstaller", "openandroidinstaller/openandroidinstaller.py"]
        + pyinstaller_options,
        shell=False,
    )
    return res


def build_macos():
    """Build on MacOS."""
    added_data = [f"--add-data={src}:{dst}" for src, dst in added_files]
    pyinstaller_options = [
        "--onefile",
        "--noconsole",
        "--noconfirm",
        "--windowed",
        "--clean",
        "--icon=openandroidinstaller/assets/favicon.ico",
        "--paths=openandroidinstaller",
    ] + added_data

    logger.info(f"Running pyinstaller with: {' '.join(pyinstaller_options)}")
    res = subprocess.check_output(
        ["pyinstaller", "openandroidinstaller/openandroidinstaller.py"]
        + pyinstaller_options,
        stderr=subprocess.STDOUT,
        shell=False,
    )
    return res


def build_windows():
    """Build on windows."""
    added_data = [f"--add-data={src};{dst}" for src, dst in added_files]
    pyinstaller_options = [
        "--onefile",
        "--noconsole",
        "--noconfirm",
        "--windowed",
        "--clean",
        "--icon=openandroidinstaller/assets/favicon.ico",
        "--paths=openandroidinstaller",
    ] + added_data

    logger.info(f"Running pyinstaller with: {' '.join(pyinstaller_options)}")
    res = subprocess.check_output(
        ["pyinstaller", "openandroidinstaller/openandroidinstaller.py"]
        + pyinstaller_options,
        stderr=subprocess.STDOUT,
        shell=False,
    )
    return res


def build():
    """Run the build for your OS and save it in the current directory."""
    if sys.platform.startswith("linux"):
        logger.info("Building for Linux")
        res = build_linux()
    elif sys.platform.startswith("darwin"):
        logger.info("Building for macOS")
        res = build_macos()
    elif sys.platform.startswith("win"):
        logger.info("Building for Windows")
        build_windows()
    else:
        raise RuntimeError("Unsupported operating system")


if __name__ == "__main__":
    build()
