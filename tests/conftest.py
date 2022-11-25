import pytest
from pathlib import Path


@pytest.fixture
def config_path():
    return Path("openandroidinstaller/assets/configs")
