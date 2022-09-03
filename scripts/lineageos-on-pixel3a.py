"""Script to flash a google pixel 3a.

Example usage:


"""
import click
from subprocess import call

from utils import run_fastboot_command


@click.command()
@click.option('--recovery', help='Path to the recovery file to flash. (Can be TWRP)')
@click.option('--image', help='Path to the lineage os image to flash.')
def install_lineage_os(recovery: str, image: str):
    unlocking_bootloader_result = unlock_bootloader()


def reboot_device():
    """Reboot the connected device."""
    click.echo("\nRunning: fastboot reboot")
    if call('fastboot' + ' reboot', shell=True) < 0:
        click.echo("*** Reboot command failed! ***")
        return 4
    return 0


def reboot_device_into_bootloader():
    """Reboot the connected device back into fastboot."""
    click.echo("\nRunning: fastboot reboot-bootloader")
    if call('fastboot reboot bootloader', shell=True) < 0:
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
    # list devices
    devices = run_fastboot_command(cmd="devices")
    click.echo(f"Found: {devices}")
    # actually unlock the bootloader
    unlock_res = run_fastboot_command(cmd="flashing unlock")
    click.echo(f"{unlock_res}")
    # reboot device
    reboot_res = reboot_device()
    if reboot_res == 4:
        click.echo("Unlocking the bootloader failed while final reboot. Exiting.")
        return False
    click.echo("Bootloader is now unlocked!")
    click.echo(">>Since the device resets completely, you will need to re-enable USB debugging to continue.")



if __name__ == '__main__':
    install_lineage_os()
