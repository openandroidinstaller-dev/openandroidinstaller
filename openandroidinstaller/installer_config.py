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

from pathlib import Path
from typing import List, Optional

import schema
import yaml
from loguru import logger
from schema import Regex, Schema, SchemaError


class Step:
    """Class representing on step in the installer."""

    default_images = {
        "Unlock the bootloader": "unlock-bootloader-default.png",
    }

    def __init__(
        self,
        title: str,
        type: str,
        content: str,
        allow_skip: bool = False,
        command: Optional[str] = None,
        img: Optional[str] = None,
        link: Optional[str] = None,
    ):
        self.title = title
        self.type = type
        self.content = content
        self.command = command
        self.img = img if img else self.default_images.get(title, "placeholder.png")
        self.allow_skip = allow_skip
        self.link = link


class InstallerConfig:
    def __init__(
        self,
        unlock_bootloader: List[Step],
        boot_recovery: List[Step],
        metadata: dict,
        requirements: dict,
    ):
        self.unlock_bootloader = unlock_bootloader
        self.boot_recovery = boot_recovery
        self.metadata = metadata
        self.requirements = requirements
        self.device_code = metadata.get("device_code")
        self.is_ab = metadata.get("is_ab_device", False)
        self.additional_steps = metadata.get("additional_steps")
        self.supported_device_codes = metadata.get("supported_device_codes")
        self.twrp_link = metadata.get("twrp-link")

    @classmethod
    def from_file(cls, path):
        with open(path, "r", encoding="utf-8") as stream:
            try:
                raw_config = yaml.safe_load(stream)
                if validate_config(raw_config):
                    config = dict(raw_config)
                    raw_steps = config["steps"]
                    metadata = config["metadata"]
                    requirements = config.get("requirements", None)
                else:
                    logger.error(f"Validation of config at {path} failed.")
                    return None
            except yaml.YAMLError as exc:
                logger.error(f"Loading the config from {path} failed with {exc}")
                return None

        if raw_steps.get("unlock_bootloader") is not None:
            unlock_bootloader = [
                Step(**raw_step, title="Unlock the bootloader")
                for raw_step in raw_steps.get("unlock_bootloader")
            ]
        else:
            unlock_bootloader = []
        boot_recovery = [
            Step(**raw_step, title="Boot custom recovery")
            for raw_step in raw_steps.get("boot_recovery", [])
        ]
        return cls(unlock_bootloader, boot_recovery, metadata, requirements)


def _find_config_file(device_code: str, config_path: Path) -> Optional[Path]:
    """Find the config file which is supported by the given device code."""
    for path in config_path.glob("*.yaml"):
        with open(path, "r", encoding="utf-8") as stream:
            try:
                raw_config = dict(yaml.safe_load(stream))
                if device_code in raw_config.get("metadata", dict()).get(
                    "supported_device_codes", []
                ):
                    logger.info(
                        f"Device code '{device_code}' is supported by config '{path}'."
                    )
                    return path
            except:
                pass
    return None


def _load_config(device_code: str, config_path: Path) -> Optional[InstallerConfig]:
    """
    Function to load a function from given path and directory path.

    Try to load local file in the same directory as the executable first, then load from assets.
    """
    custom_path = _find_config_file(device_code, config_path=Path.cwd())
    if custom_path:
        config = InstallerConfig.from_file(custom_path)
        logger.info(f"Loaded custom device config from {custom_path}.")
        logger.info(f"Config metadata: {config.metadata}.")
        return config
    else:
        # if no localfile, then try to load a config file from assets
        path = _find_config_file(device_code, config_path)

        if path:
            config = InstallerConfig.from_file(path)
            logger.info(f"Loaded device config from {path}.")
            if config:
                if "additional_steps" not in config.metadata:
                    config.metadata.update({"additional_steps": "[]"})
                logger.info(f"Config metadata: {config.metadata}.")
            return config
        else:
            logger.info(f"No device config found for device code '{device_code}'.")
            return None


def validate_config(config: str) -> bool:
    """Validate the schema of the config."""

    step_schema = {
        "type": Regex(
            r"text|confirm_button|call_button|call_button_with_input|link_button_with_confirm"
        ),
        "content": str,
        schema.Optional("command"): Regex(
            r"""adb_reboot|adb_reboot_bootloader|adb_reboot_download|adb_sideload|adb_twrp_wipe_and_install|adb_twrp_copy_partitions|fastboot_boot_recovery|fastboot_flash_boot|fastboot_flash_recovery|
            fastboot_unlock_critical|fastboot_unlock_with_code|fastboot_get_unlock_data|fastboot_unlock|fastboot_oem_unlock|fastboot_reboot|fastboot_reboot_recovery|heimdall_flash_recovery|fastboot_flash_additional_partitions"""
        ),
        schema.Optional("allow_skip"): bool,
        schema.Optional("img"): str,
        schema.Optional("link"): str,
    }

    config_schema = Schema(
        {
            "metadata": {
                "maintainer": str,
                "device_name": str,
                "is_ab_device": bool,
                "device_code": str,
                "supported_device_codes": [str],
                schema.Optional("twrp-link"): str,
                schema.Optional("additional_steps"): [
                    Regex(r"dtbo|vbmeta|vendor_boot|super_empty")
                ],
                schema.Optional("notes"): str,
                schema.Optional("brand"): str,
            },
            schema.Optional("requirements"): {
                schema.Optional("android"): schema.Or(str, int),
                schema.Optional("firmware"): str,
            },
            "steps": {
                "unlock_bootloader": schema.Or(None, [step_schema]),
                "boot_recovery": [step_schema],
            },
        }
    )
    try:
        config_schema.validate(config)
        logger.success("Config is valid.")
        return True
    except SchemaError as se:
        logger.error(f"Config is invalid. Error {se}")
        return False
