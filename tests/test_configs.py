"""Test existing config files for schema."""

import pytest
import yaml
from pathlib import Path
from openandroidinstaller.installer_config import validate_config


@pytest.mark.parametrize(
    "config_path,valid",
    [(path, True) for path in Path("openandroidinstaller/assets/configs").iterdir()],
)
def test_config(config_path: Path, valid: bool):
    """Test if the exisitng configs are valid."""
    with open(config_path, "r") as stream:
        raw_config = yaml.safe_load(stream)
    assert valid == validate_config(raw_config)
