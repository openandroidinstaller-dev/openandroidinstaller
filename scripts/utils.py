"""Reusable functions for flashing."""
from subprocess import check_output, STDOUT


def run_fastboot_command(cmd: str) -> str:
    """Run a fastboot command and return the result as string."""
    return check_output(['fastboot', cmd], stderr=STDOUT).decode()