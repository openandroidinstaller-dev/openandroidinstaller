"""Reusable functions for flashing."""
from typing import List
from subprocess import check_output, STDOUT


def run_fastboot_command(cmd: List[str]) -> str:
    """Run a fastboot command and return the result as string."""
    return check_output(["fastboot"] + cmd, stderr=STDOUT).decode()
