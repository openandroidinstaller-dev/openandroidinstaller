"""Script to flash a sony xperia z.

Example usage:
    poetry run python scripts/lineageos-on-sony-xperia-z.py --recovery images/sony-xperia-z/twrp-3.6.2_9-0-yuga.img --image images/sony-xperia-z/lineage-18.1-20220214-UNOFFICIAL-yuga.zip 
"""

# This file is part of OpenAndroidInstaller.
# OpenAndroidInstaller is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# OpenAndroidInstaller is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with OpenAndroidInstaller.
# If not, see <https://www.gnu.org/licenses>."""
# Author: Tobias Sterbak

from subprocess import call

import click
from utils import run_fastboot_command


@click.command()
@click.option("--recovery", help="Path to the recovery file to flash. (Can be TWRP)")
@click.option("--image", help="Path to the lineage os image to flash.")
def install_lineage_os(recovery: str, image: str):
    # Steps 1: Unlock the bootloader
    unlock_result = unlocking_bootloader_result = unlock_bootloader()
    if not unlock_result:
        click.echo("Unlocking the bootloader failed. Exiting.")
        return False

    # Step 2: Temporarily booting a custom recovery using fastboot
    boot_recovery_result = boot_recovery(recovery)
    if not boot_recovery_result:
        click.echo("Flashing recovery failed. Exiting.")
        return False

    # Step 3: Installing LineageOS from recovery
    install_result = install_os(image)
    if not install_result:
        click.echo("Installing LineageOS failed. Exiting.")
        return False

    click.echo("Installing lineageOS was successful! Have fun with your device! :)")
    return True


def install_os(image: str):
    """Installing LineageOS from recovery with the image filepath given in image."""
    # reboot into fastboot mode
    reboot_res = reboot_device_into_bootloader()
    if reboot_res == 4:
        click.echo("Booting into bootloader failed. Exiting.")
        return False
    # needs screen interaction here
    confirmed = click.confirm(
        "Select 'Boot into Recovery' on your smartphone screen. Wait until you are in recovery, then confirm",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )

    # automatic factory reset
    # factory_reset_result = run_fastboot_command(cmd=["erase", "cache"])
    # click.echo(f"{factory_reset_result}")
    # factory_reset_result = run_fastboot_command(cmd=["erase", "userdata"])
    # click.echo(f"{factory_reset_result}")

    # manual factory reset
    confirmed = click.confirm(
        "Now tap Factory Reset, then Format data / factory reset and continue with the formatting process. This will remove encryption and delete all files stored in the internal storage, as well as format your cache partition (if you have one). Confirm if you are done",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )

    # sideload linageos image with adb
    confirmed = click.confirm(
        "On the device, select “Apply Update”, then “Apply from ADB” to begin sideload. Then confirm here",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    click.echo("\nRunning: adb sideload <image>")
    if call(f"adb sideload {image}", shell=True) < 0:
        click.echo("*** Sideloading image failed! ***")
        return False

    click.echo(
        "Flashing finished. Now press 'back' (arrow) and then 'Reboot system now' to finish the installation."
    )
    return True


def boot_recovery(recovery: str):
    """
    Temporarily booting a custom recovery using fastboot.

    Using the recovery found in the path 'recovery'.
    """
    # reboot into fastboot mode
    reboot_res = reboot_device_into_bootloader()
    if reboot_res == 4:
        click.echo("Unlocking the bootloader failed. Exiting.")
        return False
    # needs screen interaction here
    confirmed = click.confirm(
        "Select 'Restart bootloader' on your smartphone screen. Then confirm",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    # list devices
    devices = run_fastboot_command(cmd=["devices"])
    click.echo(f"Found: {devices}")
    # flash the recovery (temporarily)
    flash_result = run_fastboot_command(cmd=["flash", "boot", recovery])
    click.echo("Recovery flashed successfully.")
    return True


def reboot_device():
    """Reboot the connected device."""
    click.echo("\nRunning: fastboot reboot")
    if call("fastboot" + " reboot", shell=True) < 0:
        click.echo("*** Reboot command failed! ***")
        return 4
    return 0


def reboot_device_into_bootloader():
    """Reboot the connected device into fastboot."""
    click.echo("\nRunning: adb reboot bootloader")
    if call("adb reboot bootloader", shell=True) < 0:
        click.echo("*** Reboot-bootloader command failed! ***")
        return 4
    return 0


def unlock_bootloader():
    """Function to unlock the bootloader."""
    # reboot into fastboot mode
    reboot_res = reboot_device_into_bootloader()
    if reboot_res == 4:
        click.echo("Unlocking the bootloader failed. Exiting.")
        return False
    # needs screen interaction here
    confirmed = click.confirm(
        "Select 'Restart bootloader' on your smartphone screen. Then confirm",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    # list devices
    devices = run_fastboot_command(cmd=["devices"])
    click.echo(f"Found: {devices}")
    # actually unlock the bootloader
    unlock_res = run_fastboot_command(cmd=["flashing", "unlock"])
    click.echo(f"{unlock_res}")
    click.confirm(
        "At this point the device may display on-screen prompts which will require interaction to continue the process of unlocking the bootloader. Please take whatever actions the device asks you to to proceed.",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    # reboot device
    reboot_res = reboot_device()
    if reboot_res == 4:
        click.echo("Unlocking the bootloader failed while final reboot. Exiting.")
        return False
    click.echo("Bootloader is now unlocked!")
    click.echo(
        ">>Since the device resets completely, you will need to re-enable USB debugging to continue."
    )
    confirmed = click.confirm(
        "Confirm to continue",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    return confirmed


if __name__ == "__main__":
    install_lineage_os()
