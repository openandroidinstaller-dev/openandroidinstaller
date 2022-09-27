"""Basic script to get adb and fastboot.

Inspired by: https://gitlab.com/ubports/installer/android-tools-bin/-/blob/master/build.js
"""
import requests
from pathlib import Path
import zipfile
from io import BytesIO


def download_adb_fastboot(platform: str):
    url = f"https://dl.google.com/android/repository/platform-tools-latest-{platform}.zip"
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)
    # Split URL to get the file name
    filename = url.split('/')[-1]
 
    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("tools")).resolve()
    file = zipfile.ZipFile(BytesIO(response.content))
    file.extractall(download_path.name)
    return filename 


def download_heimdall(platform: str):
    url = f"https://people.ubuntu.com/~neothethird/heimdall-{platform}.zip"
    # Downloading the file by sending the request to the URL
    response = requests.get(url, allow_redirects=True)
    # Split URL to get the file name
    filename = url.split('/')[-1]
 
    # Writing the file to the local file system
    download_path = Path(__file__).parent.joinpath(Path("heimdall")).resolve()
    file = zipfile.ZipFile(BytesIO(response.content))
    file.extractall(download_path.name)
    return filename 



def move_files_to_lib():
    target_path = Path("openandroidinstaller/bin", exist_ok=True)
    target_path.mkdir()
    # move adb
    adb_path = Path(__file__).parent.joinpath(Path("../tools/platform-tools/adb")).resolve()
    adb_target_path = Path(__file__).parent.joinpath(Path("../openandroidinstaller/bin/adb")).resolve()
    adb_path.rename(adb_target_path)
    # move fastboot
    fb_path = Path(__file__).parent.joinpath(Path("../tools/platform-tools/fastboot")).resolve()
    fb_target_path = Path(__file__).parent.joinpath(Path("../openandroidinstaller/bin/fastboot")).resolve()
    fb_path.rename(fb_target_path)
    # move heimdall
    hd_path = Path(__file__).parent.joinpath(Path("../heimdall/heimdall")).resolve()
    hd_target_path = Path(__file__).parent.joinpath(Path("../openandroidinstaller/bin/heimdall")).resolve()
    hd_path.rename(hd_target_path)
    # make executable
    adb_target_path.chmod(0o755)
    fb_target_path.chmod(0o755)
    hd_target_path.chmod(0o755)
    print("Done")
    

def main():
    filename = download_adb_fastboot(platform="linux")
    print(filename)
    filename = download_heimdall(platform="linux")
    move_files_to_lib()


if __name__ == "__main__":
    main()