<br />
<div align="center">
  <h1>OpenAndroidInstaller</h1>

  [![License](https://img.shields.io/github/license/openandroidinstaller-dev/openandroidinstaller?color=green&style=flat-square)](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/LICENSE)
  [![Release](https://img.shields.io/github/v/release/openandroidinstaller-dev/openandroidinstaller?include_prereleases&style=flat-square)](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases)
  [![Downloads](https://img.shields.io/github/downloads/openandroidinstaller-dev/openandroidinstaller/total?style=flat-square)](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases)
  [![Twitter](https://img.shields.io/twitter/follow/oainstaller?style=social)](https://twitter.com/OAInstaller)
  [![Mastodon](https://img.shields.io/mastodon/follow/109341220262803943?domain=https%3A%2F%2Ffosstodon.org&style=social)](https://fosstodon.org/@openandroidinstaller)
  <p>Makes installing alternative Android distributions nice and easy.</p>
  <a href="https://github.com/openandroidinstaller-dev/openandroidinstaller">
    <img src="openandroidinstaller/assets/logo-192x192.png" alt="OpenAndroidInstaller" height="80">
  </a>

  <p align="center">
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

> **Warning**: This application is currently in early alpha state, so use at your own risk! I take no responsibility for bricked devices or dead SD cards.

> **Note**: Unlocking the bootloader will erase all data on your device!
This also includes your DRM keys, which are stored in the Trim Area partition (also called TA).
Before proceeding, ensure the data you would like to retain is backed up to your PC and/or your Google account, or equivalent. Please note that OEM backup solutions like Samsung and Motorola backup may not be accessible from LineageOS once installed.
If you wish to backup the TA partition first, you can find tutorials related to your device on the internet.

## Officially supported devices
Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Samsung | Galaxy A3 2017 | a3y17lte | SM-A320FL | tested
Samsung | Galaxy A5 2016 | a5xelte | SM-A510F | tested
Samsung | Galaxy S7 | herolte | SM-G930F | tested
Samsung | Galaxy S9 | starlte | | under development
Google | Pixel 3a | sargo | sargo | tested
Google | Pixel 4a | sunfish | sunfish | planned
Sony | Xperia Z | yuga | C6603 | tested
Sony | Xperia Z3 | z3 | | under development
Sony | Xperia ZX | kagura | | planned
Fairphone | Fairphone 2 | FP2 | | under development
Fairphone | Fairphone 3 | FP3 | | tested
Motorola | moto G5 | cedric | | planned
Motorola | moto g7 power | ocean | | under development


## Usage

Linux is currently the best supported platform (tested with Ubuntu 20.04 LTS). Windows and MacOS are also supported but you might experience more issues. So far there is no support for ARM-based systems.

1. Download the AppImage, .exe or appropriate executable file for your OS. You might need to change permissions to run the executable.
    - On Windows also [install the Universal USB Drivers](https://adb.clockworkmod.com/) and other potentially drivers needed for your device.
2. Download the lineageOS image and the custom recovery image. A source for files can be found on https://wiki.lineageos.org/devices/ or you can just search the web for an appropriate version for your device.
3. Start the desktop app and follow the instructions.


## Run OpenAndroidInstaller for development

Currently development is only supported on Ubuntu Linux. MacOS and Windows should also work fine. You might need to install additional USB-drivers on Windows.

1. Clone the main branch of this repository
2. Run `make poetry` and `make install` to install poetry to manage python and install the required dependencies like adb, fastboot and heimdall.
3. Run `make app` to start the desktop app from the source.


## Contributing

All kinds of contributions are welcome. These include:
- Fix and improve texts in configs and in the application.
- Test the tool for a supported device.
- Create a config for a new device.
- Test the application on your computer.
- Contribute an application build for a new platform.

### How to contribute your own installation configurations

If you want to use the tool for a non-supported smartphone, the fastest way is to adapt an [existing config file](https://github.com/openandroidinstaller-dev/openandroidinstaller/tree/main/openandroidinstaller/assets/configs). The file should be named after the `device code` of your device. This is in general the output by `adb shell getprop | grep ro.product.device` when the devices is connected to the computer. You can also get the device code by connecting the device to the computer and run OpenAndroidInstaller to detect the device.

**To test your config file with the executable** without using the developer setup, place it in the same directory as the executable. There it will be detected by name. After you created a config file and it works fine, you can open a pull request to make the file available to other users. Please also add the device to the supported devices table above.

#### Content of a config file

Every step in the config file corresponds to one view in the application. These steps should contain the following fields:
- `type`: str; Corresponds to the type of view to generate. There are the following options:
  - `text`: Just display the text given in content.
  - `confirm_button`: Display the content, as well as a button to allow the user to go to the next step.
  - `call_button`: Display the content text and a button that runs a given command. After the command is run, a confirm button is displayed to allow the user to move to the next step.
  - `call_button_with_input`: Display the content text, an input field and a button that runs a given command. The inputtext, can be used in the command by using the `<inputtext>` placeholder in the command field. After the command is run, a confirm button is displayed to allow the user to move to the next step.
  - `link_button_with_confirm`: Display a button that opens a browser with a given link, confirm afterwards. Link is given in `link`.
- `content`: str; The content text displayed alongside the action of the step. Used to inform the user about whats going on.
- `command`: [ONLY for call_button* steps] str; The command to run. One of `adb_reboot`, `adb_reboot_bootloader`, `adb_reboot_download`, `adb_sideload`, `adb_twrp_wipe_and_install`, `fastboot_flash_recovery`, `fastboot_unlock_with_code`, `fastboot_unlock`, `fastboot_oem_unlock`, `fastboot_reboot`, `heimdall_flash_recovery`.
- `img`: [OPTIONAL] Display an image on the left pane of the step view. Images are loaded from `openandroidinstaller/assets/imgs/`.
- `allow_skip`: [OPTIONAL] boolean; If a skip button should be displayed to allow skipping this step. Can be useful when the bootloader is already unlocked.
- `link`: [OPTIONAL] Link to use for the link button if type is `link_button_with_confirm`.

### How to build the application for your platform

The executables for the OpenAndroidInstaller are build with [pyinstaller](https://pyinstaller.org/en/stable/index.html). You can create builds for MacOS or Linux with `make build-app`. For Windows the paths need to be modified. For now, you can have a look [here](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/v0.1.2-alpha/.github/workflows/manual-build-windows.yml#L22) on how it's done.

If you build the application for your platform and want to contribute the build, please reach out to me.

#### On unlocking the bootloader
Devices by *Samsung*, *Google* and *Fairphone* make it fairly easy to unlock the bootloader and receive good support in the installer.

Some devices with require manual steps to unlock the bootloader. In general you will need to create an account at a vendor website and receive some code from there. OpenAndroidInstaller will try to guide you as far as possible. These vendors include *Sony, Motorola, Xiaomi* among others.

Other phone vendors stops allowing to unlock the bootloader all together. There is nothing to be done if you didn't unlock your device in time. These vendors include *Huawei and LG* among others. Support for these vendors will always be very limited.

## Tools

- The [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) (such as adb and fastboot) are [Apache](https://android.googlesource.com/platform/system/adb/+/refs/heads/master/NOTICE)-licensed universal Android utilities
- [Heimdall](https://gitlab.com/BenjaminDobell/Heimdall/) is an [MIT](https://gitlab.com/BenjaminDobell/Heimdall/-/blob/master/LICENSE)-licensed replacement for the leaked ODIN tool to flash Samsung devices.
- [libusb-1.0](https://github.com/libusb/libusb) is a [LGPL-2.1](https://github.com/libusb/libusb/blob/master/COPYING)-licensed library for USB device access from Linux, macOS, Windows and others.


## Acknowledgements

* Funded from September 2022 until February 2023 by ![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)


## License
Original development by [Tobias Sterbak](https://tobiassterbak.com). Copyright (C) 2022.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
