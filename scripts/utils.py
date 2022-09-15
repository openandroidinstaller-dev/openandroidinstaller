"""Reusable functions for flashing."""
from subprocess import STDOUT, check_output
from typing import List


def run_fastboot_command(cmd: List[str]) -> str:
    """Run a fastboot command and return the result as string."""
    return check_output(["fastboot"] + cmd, stderr=STDOUT).decode()
