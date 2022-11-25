"""Test existing config files for schema."""

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

import pytest
import yaml

from openandroidinstaller.installer_config import validate_config, _load_config


@pytest.mark.parametrize(
    "config_path,valid",
    [(path, True) for path in Path("openandroidinstaller/assets/configs").iterdir()],
)
def test_config(config_path: Path, valid: bool):
    """Test if the existing configs are valid."""
    with open(config_path, "r") as stream:
        raw_config = yaml.safe_load(stream)
    assert valid == validate_config(raw_config)


def test_load_config_valid(config_path):
    """Test if a valid config can be loaded."""
    config = _load_config(device_code="sargo", config_path=config_path)

    # assert some properties of the config
    assert config
    assert config.metadata.get("devicecode") == "sargo"


def test_load_config_notfound(config_path):
    """Test if the function properly escalates when a config is not found."""
    config = _load_config(device_code="nothing", config_path=config_path)

    # assert some properties of the config
    assert config == None
