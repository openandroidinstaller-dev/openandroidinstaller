<br />
<div align="center">
  <h1>OpenAndroidInstaller</h1>
  <a href="https://github.com/openandroidinstaller-dev/openandroidinstaller">
    <img src="openandroidinstaller/assets/logo-192x192.png" alt="OpenAndroidInstaller" height="80">
  </a>

  <p align="center">
    <br />
    Makes installing alternative Android distributions nice and easy.
    <br />
    The OpenAndroidInstaller project helps Android users to keep their smartphone's operating system up to date with free software and to continue using the device even though the manufacturer no longer offers updates. With a graphical installation software, users are easily guided through the installation process of free Android operating systems like LineageOS.
    <br />
    <br />
    <a href="https://github.com/openandroidinstaller-dev/openandroidinstaller/issues">Report Bug</a>
    ·
    <a href="https://openandroidinstaller.org">Website</a>
    ·
    <a href="mailto: hello@openandroidinstaller.org">Request Feature</a>
    <br />
  </p>
</div>


## Warning: Unlocking the bootloader will erase all data on your device!
This also includes your DRM keys, which are stored in the Trim Area partition (also called TA).
Before proceeding, ensure the data you would like to retain is backed up to your PC and/or your Google account, or equivalent. Please note that OEM backup solutions like Samsung and Motorola backup may not be accessible from LineageOS once installed.
If you wish to backup the TA partition first, you can find tutorials related to your device on the internet.

## Officially supported devices
Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Samsung | Galaxy A3 2017 | a3y17lte | SM-A320FL | tested
Samsung | Galaxy A5 2016 | a5xelte |  | under development
Google | Pixel 3a | sargo | sargo | tested
Sony | Xperia Z | yuga | | tested

## Installation

1. Download the AppImage, .exe or appropriate file for your OS. 
2. Install `adb` and `fastboot` by running `sudo apt install android-tools-adb android-tools-fastboot`
3. OPTIONAL: Install `heimdall` for Samsung Devices:
    - download heimdall: https://androidfilehost.com/?w=files&flid=304516
    - install heimdall: 
        $ unzip /path/to/heimdall_ubuntu.zip -d /tmp
        $ cp /tmp/bin/heimdall* /usr/bin/
        $ rm -rf /tmp/bin

## Usage

Download the lineageOS image and the custom recovery image.
Start the desktop app and follow the instructions.

## Run OpenAndroidInstaller for development

1. Clone the main branch of this repository
2. Run `make poetry` and `make install` to setup poetry and the relevant requirements
3. Clone this Run `make app` to start the desktop app from the source code.

## Add your own installation configurations

## Contributing

## Acknowledgements

* Funded from September 2022 until February 2023 by ![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)