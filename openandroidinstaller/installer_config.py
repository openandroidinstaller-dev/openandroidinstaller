"""Class to load config files for the install procedure."""

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

from typing import List, Optional
from pathlib import Path
from loguru import logger

import yaml


class Step:
    def __init__(
        self,
        title: str,
        type: str,
        content: str,
        command: str = None,
        img: str = "placeholder.png",
        allow_skip: bool = False,
    ):
        self.title = title
        self.type = type
        self.content = content
        self.command = command
        self.img = img
        self.allow_skip = allow_skip


class InstallerConfig:
    def __init__(self, steps: List[Step], metadata: dict):
        self.steps = steps
        self.metadata = metadata

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as stream:
            try:
                raw_config = yaml.safe_load(stream)
                config = dict(raw_config)
                raw_steps = config["steps"]
                metadata = config["metadata"]
            except yaml.YAMLError as exc:
                print(exc)

        steps = [Step(**raw_step) for raw_step in raw_steps]
        return cls(steps, metadata)


def _load_config(device_code: str, config_path: Path) -> Optional[InstallerConfig]:
    """
    Function to load a function from given path and directory path.
    
    Try to load local file in the same directory as the executable first, then load from assets.
    """
    # try loading a custom local file first
    custom_path = Path.cwd().joinpath(Path(f"{device_code}.yaml"))
    try:
        config = InstallerConfig.from_file(custom_path)
        logger.info(f"Loaded custom device config from {custom_path}.")
        logger.info(f"Config metadata: {config.metadata}.")
        return config
    except FileNotFoundError:
        # if no localfile, then try to load a config file from assets
        path = config_path.joinpath(Path(f"{device_code}.yaml"))
        try:
            config = InstallerConfig.from_file(path)
            logger.info(f"Loaded device config from {path}.")
            logger.info(f"Config metadata: {config.metadata}.")
            return config
        except FileNotFoundError:
            logger.info(f"No device config found for {path}.")
            return None
