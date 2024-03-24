"""Script to flash a Samsung Galaxy A3 (2017).

Following: https://lineageosroms.com/a3xelte/#basic-requirements

Example usage:
    poetry run python scripts/lineageos-on-galaxy-a3.py --recovery images/samsung-galaxy-a3/twrp-3.6.2_9-0-a3y17lte.img --image images/samsung-galaxy-a3/lineage-16.0-20190908-UNOFFICIAL-a3y17lte.zip
"""

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
from subprocess import call
from time import sleep

import click


@click.command()
@click.option("--recovery", help="Path to the recovery file to flash. (Can be TWRP)")
@click.option("--image", help="Path to the lineage os image to flash.")
def install_lineage_os(recovery: str, image: str):
    """Main function to install lineage os."""
    click.echo("Install lineage os on Samsung Galaxy A3.")
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
    # manual wiping and stuff
    click.echo("Now tap 'Wipe'.")
    sleep(2)
    click.echo(
        "Then tap 'Format Data' and continue with the formatting process. This will remove encryption and delete all files stored in the internal storage."
    )
    sleep(2)
    click.echo(
        "Return to the previous menu and tap 'Advanced Wipe', then select the 'Cache' and 'System' partitions and then 'Swipe to Wipe'."
    )
    confirmed = click.confirm(
        "Confirm to continue",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )

    # sideload lineage os image with ADB
    confirmed = click.confirm(
        "On the device, select “Advanced”, “ADB Sideload”, then swipe to begin sideload. Then confirm here",
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

    # (Optionally): If you want to install any additional add-ons, repeat the sideload steps above for those packages in sequence.

    confirmed = click.confirm(
        "Confirm to continue",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )

    click.echo("\nRebooting")
    if call("adb reboot", shell=True) < 0:
        return False

    click.echo("Flashing finished.")
    return True


def boot_recovery(recovery: str):
    """
    Temporarily booting a custom recovery using fastboot.

    Using the recovery found in the path 'recovery'.
    """
    # check if heimdall is installed.
    heimdall_res = check_heimdall()
    if heimdall_res == 4:
        click.echo("No heimdall found. Exiting.")
        return False

    # reboot into download mode
    click.confirm(
        "Turn on your device and wait until its fully booted.",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    click.echo("\nBooting into download mode:")
    if call("adb reboot download", shell=True) < 0:
        click.echo("*** Booting into download mode failed! ***")
        return False
    confirmed = click.confirm(
        "Confirm to continue",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )

    # install TWRP recovery from image
    click.echo("\nFlash custom recovery")
    if call(f"heimdall flash --no-reboot --RECOVERY {recovery}", shell=True) < 0:
        click.echo("*** Flashing custom recovery failed! ***")
        return False
    click.echo(
        "A blue transfer bar will appear on the device showing the recovery image being flashed."
    )
    sleep(5)
    click.echo("Once it's done, unplug the USB cable from your device.")
    click.echo(
        "Manually reboot into recovery. Press the Volume Down + Power buttons for 8~10 seconds until the screen turns black & release the buttons immediately when it does, then boot to recovery with the device powered off, hold Volume Up + Home + Power."
    )
    confirmed = click.confirm(
        "Confirm to continue",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )

    click.echo("Recovery flashed successfully.")
    return True


def unlock_bootloader():
    """Function to unlock the bootloader."""
    confirmed = click.confirm(
        "Turn on developer options and OEM Unlock on your phone.",
        default=True,
        abort=False,
        prompt_suffix=": ",
        show_default=True,
        err=False,
    )
    # click.echo("Now, turn of your phone. Then press Volume Up and Power key for a couple of seconds. All your data will be deleted!")
    # click.echo("Release both keys when the SAMSUNG Galaxy A3 Core logo pops up.")
    # click.confirm("After that choose Reboot to bootloader by using Volume keys to scroll down and the Power button to confirm that. ",
    #              default=True, abort=False, prompt_suffix=': ', show_default=True, err=False)
    return confirmed


def check_heimdall():
    """Check if heimdall is installed properly."""
    if call("heimdall info", shell=True) != 0:
        click.echo("*** Heimdall is not properly installed. Exiting.")
        return 4
    return 0


if __name__ == "__main__":
    install_lineage_os()
