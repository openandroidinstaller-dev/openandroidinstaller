"""Check if adb works and print the version."""
from subprocess import check_output, STDOUT


def check_adb_version():
    return check_output(["adb", "version"], stderr=STDOUT).decode()


if __name__ == "__main__":
    print("Checking if adb is installed...")
    adb_version = check_adb_version()
    if adb_version:
        print(adb_version)
        print("Done.")
    else:
        print("Failed.")
