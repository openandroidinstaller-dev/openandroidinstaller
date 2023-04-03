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

> **Warning**: This application is currently in beta state, so use at your own risk! While many people tested the application so far and we heard of no bricked devices, things might still go wrong.

> **Note**: Unlocking the bootloader will erase all data on your device!
This also includes your DRM keys, which are stored in the Trim Area partition (also called TA) in case your device is fairly recent and supports DRM L1. Those devices will be downgraded to DRM L3. Devices on DRM L3 by default will not be affected.
Before proceeding, ensure the data you would like to retain is backed up to your PC and/or your Google account, or equivalent. Please note that OEM backup solutions like Samsung and Motorola backup may not be accessible from LineageOS once installed.
If you wish to backup the TA partition first, you can find tutorials related to your device on the internet.


## Usage

Linux is currently the best supported platform (tested with Ubuntu 20.04/22.04 LTS). Windows and MacOS are also supported but you might experience more issues. So far there is no support for ARM-based systems.

1. Download the AppImage, .exe or appropriate executable file for your OS. You might need to change permissions to run the executable.
    - On Windows also [install the Universal USB Drivers](https://adb.clockworkmod.com/) and other potentially drivers needed for your device.
2. Download the custom ROM image and the TWRP recovery image for your device and optionally some addons. A source for files can be found on the following websites:
    - some custom ROMs:
      - [LineageOS](https://wiki.lineageos.org/devices/)
      - [/e/OS](https://doc.e.foundation/devices)
      - [LineageOS for microg](https://download.lineage.microg.org/)
      - [BlissRoms](https://blissroms.org/)
      - [PixelExperience](https://download.pixelexperience.org/)
    - TWRP Recovery:
      - [TWRP recovery](https://twrp.me/Devices/)
    - Optional Addons:
      - There are different packages of *Google Apps* available.
        - [MindTheGapps](https://wiki.lineageos.org/gapps#downloads)
        - [NikGApps](https://nikgapps.com/)
      - [MicroG](https://microg.org/)
        - The recommended way to install MicroG is to use the zip file provided here: [https://github.com/FriendlyNeighborhoodShane/MinMicroG_releases/releases](https://github.com/FriendlyNeighborhoodShane/MinMicroG_releases/releases).
      - [F-Droid App-Store](https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota/).
    - or you can just search the web or the [xda-developers forum](https://forum.xda-developers.com) for an appropriate version for your device.
3. Start the desktop app and follow the instructions.


## Officially supported devices

Currently, the **we support 57 devices** by various vendors and working on adding more soon!


Support for these devices is provided as best effort, but things might still go wrong.
Help to improve the tool by reporting any issues you might face.

<details><summary><b>Samsung</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Samsung | Galaxy J7 2015 | j7elte | | tested
Samsung | Galaxy A3 2017 | a3y17lte | SM-A320FL | tested
Samsung | Galaxy S III Neo | s3ve3g | GT-I9301I | tested
Samsung | Galaxy A5 2016 | [a5xelte](https://wiki.lineageos.org/devices/a5xelte/) | SM-A510F | tested
Samsung | Galaxy A7 2016 | a7xelte | | tested
Samsung | Galaxy S4 Mini LTE| [serranoltexx](https://wiki.lineageos.org/devices/serranoltexx/) | | tested
Samsung | Galaxy S6 | [zerofltexx](https://wiki.lineageos.org/devices/zerofltexx/) | | tested
Samsung | Galaxy S6 Edge | [zeroltexx](https://wiki.lineageos.org/devices/zeroltexx/) | | tested
Samsung | Galaxy S7 | [herolte](https://wiki.lineageos.org/devices/herolte/) | SM-G930F | tested
Samsung | Galaxy S7 Edge | [hero2lte](https://wiki.lineageos.org/devices/hero2lte/) | | tested
Samsung | Galaxy S9 | [starlte](https://wiki.lineageos.org/devices/starlte/) | | tested
Samsung | Galaxy Note 8 | greatlte | SM-N950F | tested
Samsung | Galaxy Note 9 | [crownlte](https://wiki.lineageos.org/devices/crownlte/) | | tested
Samsung | Galaxy S10 | [beyond1lte](https://wiki.lineageos.org/devices/beyond1lte/) | | tested
Samsung | Galaxy S10e | [beyond0lte](https://wiki.lineageos.org/devices/beyond0lte/) | | tested
Samsung | Galaxy S10+ | [beyond2lte](https://wiki.lineageos.org/devices/beyond2lte/) | | tested
Samsung | Galaxy Note 10 | [d1](https://wiki.lineageos.org/devices/d1/) | | tested
Samsung | Galaxy Note 10+ | [d2s](https://wiki.lineageos.org/devices/d2s/) | | tested
Samsung | Galaxy Note 3 LTE | [hltetmo](https://wiki.lineageos.org/devices/hltetmo/) | N900T/V/W8 | tested
</details>

<details><summary><b>Google</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Google | Pixel 2 | [walleye](https://wiki.lineageos.org/devices/walleye/) | walleye | tested
Google | Pixel 2 XL | [taimen](https://wiki.lineageos.org/devices/taimen/) | taimen | tested
Google | Pixel 3 | [blueline](https://wiki.lineageos.org/devices/blueline/) | blueline | tested
Google | Pixel 3 XL | [crosshatch](https://wiki.lineageos.org/devices/crosshatch/) | crosshatch | tested
Google | Pixel 3a | [sargo](https://wiki.lineageos.org/devices/sargo/) | sargo | tested
Google | Pixel 3a XL | [bonito](https://wiki.lineageos.org/devices/bonito/) | bonito | tested
Google | Pixel 4 | [flame](https://wiki.lineageos.org/devices/flame/) | flame | tested 
Google | Pixel 4 XL | [coral](https://wiki.lineageos.org/devices/coral/) | coral | tested 
Google | Pixel 4a | [sunfish](https://wiki.lineageos.org/devices/sunfish/) | sunfish | tested 
Google | Pixel 5 | [redfin](https://wiki.lineageos.org/devices/redfin/) | redfin | tested
Google | Pixel 5a | [barbet](https://wiki.lineageos.org/devices/barbet/) | barbet | tested
</details>

<details><summary><b>Sony</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Sony | Xperia Z | [yuga](https://wiki.lineageos.org/devices/yuga/) | C6603 | tested
Sony | Xperia Z3 | [z3](https://wiki.lineageos.org/devices/z3/) | | tested
Sony | Xperia 10 | [kirin](https://wiki.lineageos.org/devices/kirin/) | | tested
Sony | Xperia 10 Plus | [mermaid](https://wiki.lineageos.org/devices/mermaid/) | | tested
Sony | Xperia XA2 | [pioneer](https://wiki.lineageos.org/devices/pioneer/) | | tested
Sony | Xperia XZ2 | [akari](https://wiki.lineageos.org/devices/akari/) | | tested
Sony | Xperia XZ3 | [akatsuki](https://wiki.lineageos.org/devices/akatsuki/) | | tested
Sony | Xperia ZX | kagura | | planned
</details>

<details><summary><b>Fairphone</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Fairphone | Fairphone 2 | [FP2](https://wiki.lineageos.org/devices/FP2/) | | tested
Fairphone | Fairphone 3 | [FP3](https://wiki.lineageos.org/devices/FP3/) | | tested
Fairphone | Fairphone 4 | [FP4](https://wiki.lineageos.org/devices/FP4/) | | tested
</details>

<details><summary><b>Motorola</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Motorola | moto g5 | [cedric](https://wiki.lineageos.org/devices/cedric/) | | tested
Motorola | moto g6 plus | [evert](https://wiki.lineageos.org/devices/evert/) | | tested
Motorola | moto g7 power | [ocean](https://wiki.lineageos.org/devices/ocean/) | | tested
Motorola | moto g 5G plus / one 5G | [nairo](https://wiki.lineageos.org/devices/nairo/) | | tested
Motorola | moto g 5G / one 5G ace | [kiev](https://wiki.lineageos.org/devices/kiev/) | | tested
Motorola | edge | [racer](https://wiki.lineageos.org/devices/racer/) | | tested
Motorola | moto z | [griffin](https://wiki.lineageos.org/devices/griffin/) | | tested
</details>

<details><summary><b>OnePlus</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
OnePlus | One | [bacon](https://wiki.lineageos.org/devices/bacon/) | A0001 | tested
OnePlus | 5 | [cheeseburger](https://wiki.lineageos.org/devices/cheeseburger/) | | tested
OnePlus | 5T | [dumpling](https://wiki.lineageos.org/devices/dumpling/) | | tested
OnePlus | 6 | [enchilada](https://wiki.lineageos.org/devices/enchilada/) | | tested
OnePlus | 6T | [fajita](https://wiki.lineageos.org/devices/fajita/) | | tested
OnePlus | 7 | [guacamoleb](https://wiki.lineageos.org/devices/guacamoleb/) | | tested
OnePlus | 7 Pro | [guacamole](https://wiki.lineageos.org/devices/guacamole/) | | tested
OnePlus | 7T | [hotdogb](https://wiki.lineageos.org/devices/hotdogb/) | | tested
OnePlus | 7T Pro | [hotdog](https://wiki.lineageos.org/devices/hotdog/) | | tested
OnePlus | Nord | [avicii](https://wiki.lineageos.org/devices/avicii/) | | tested
OnePlus | Nord N200 | [dre](https://wiki.lineageos.org/devices/dre/) | | tested
OnePlus | 9 | lemonade | | under development
</details>

And more to come!


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

If you want to use the tool for a non-supported smartphone, the fastest way is to adapt an [existing config file](https://github.com/openandroidinstaller-dev/openandroidinstaller/tree/main/openandroidinstaller/assets/configs). The file should be named after the official `device code` of the device. Add the code output by `adb shell getprop | grep ro.product.device` (when the devices is connected to the computer) as well as the official device code to the `supported_device_codes` list in the config. You can also get the device code by connecting the device to the computer and run OpenAndroidInstaller to detect the device.

**To test your config file with the executable** without using the developer setup, place it in the same directory as the executable. There it will be detected by name. After you created a config file and it works fine, you can open a pull request to make the file available to other users. Please also add the device to the supported devices table above.

#### Content of a config file

A config file consists of two parts. The first part are some metadata about the device and the second parts are the steps to unlock the bootloader, boot a recovery and install the ROMs.

##### How to write Metadata
Every config file should have metadata with the following fields:
- `maintainer`: str; Maintainer and author of the config file.
- `device_name`: str; Name of the device.
- `is_ab_device`: bool; A boolean to determine if the device is a/b-partitioned or not.
- `device_code`: str; The official device code.
- `supported_device_codes`: List[str]; A list of supported device codes for the config. The config will be loaded based on this field.
- `twrp-link`: [OPTIONAL] str; name of the corresponding twrp page.

In addition to these metadata, every config can have optional requirements. If these are set, the user is asked to check if they are meet.
- `android`: [OPTIONAL] int|str; Android version to install prior to installing a custom ROM.
- `firmware`: [OPTIONAL] str; specific firmware version to install before installing a custom ROM.

##### How to write steps:
Every step in the config file corresponds to one view in the application. These steps should contain the following fields:
- `type`: str; Corresponds to the type of view to generate. There are the following options:
  - `text`: Just display the text given in content.
  - `confirm_button`: Display the content, as well as a button to allow the user to go to the next step.
  - `call_button`: Display the content text and a button that runs a given command. After the command is run, a confirm button is displayed to allow the user to move to the next step.
  - `call_button_with_input`: Display the content text, an input field and a button that runs a given command. The inputtext, can be used in the command by using the `<inputtext>` placeholder in the command field. After the command is run, a confirm button is displayed to allow the user to move to the next step.
  - `link_button_with_confirm`: Display a button that opens a browser with a given link, confirm afterwards. Link is given in `link`.
- `content`: str; The content text displayed alongside the action of the step. Used to inform the user about whats going on.
- `command`: [ONLY for call_button* steps] str; The command to run. One of `adb_reboot`, `adb_reboot_bootloader`, `adb_reboot_download`, `adb_sideload`, `adb_twrp_wipe_and_install`, `adb_twrp_copy_partitions`, `fastboot_boot_recovery`, `fastboot_unlock_with_code`, `fastboot_unlock`, `fastboot_oem_unlock`, `fastboot_get_unlock_data`, `fastboot_reboot`, `heimdall_flash_recovery`.
- `img`: [OPTIONAL] Display an image on the left pane of the step view. Images are loaded from `openandroidinstaller/assets/imgs/`.
- `allow_skip`: [OPTIONAL] boolean; If a skip button should be displayed to allow skipping this step. Can be useful when the bootloader is already unlocked.
- `link`: [OPTIONAL] Link to use for the link button if type is `link_button_with_confirm`.

You can also use the `requirements` field in the yaml, to specify `firmware` or `android` version requirements. The user will then be prompted if these requirements are satisfied. 

### How to build the application for your platform

The executables for the OpenAndroidInstaller are build with [pyinstaller](https://pyinstaller.org/en/stable/index.html). You can create builds for MacOS or Linux with `make build-app`. For Windows the paths need to be modified. For now, you can have a look [here](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/v0.1.2-alpha/.github/workflows/manual-build-windows.yml#L22) on how it's done.

If you build the application for your platform and want to contribute the build, please reach out to me.

#### On unlocking the bootloader
Devices by *Samsung*, *Google* and *Fairphone* make it fairly easy to unlock the bootloader and receive good support in the installer.

Some devices with require manual steps to unlock the bootloader. In general you will need to create an account at a vendor website and receive some code from there. OpenAndroidInstaller will try to guide you as far as possible. These vendors include *Sony, Motorola, Xiaomi* and *OnePlus* among others.

Other phone vendors stops allowing to unlock the bootloader all together. There is nothing to be done if you didn't unlock your device in time. These vendors include *Huawei and LG* among others. Support for these vendors will always be very limited.

## Tools

- The [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) (such as adb and fastboot) are [Apache](https://android.googlesource.com/platform/system/adb/+/refs/heads/master/NOTICE)-licensed universal Android utilities
- [Heimdall](https://gitlab.com/BenjaminDobell/Heimdall/) is an [MIT](https://gitlab.com/BenjaminDobell/Heimdall/-/blob/master/LICENSE)-licensed replacement for the leaked ODIN tool to flash Samsung devices.
- [libusb-1.0](https://github.com/libusb/libusb) is a [LGPL-2.1](https://github.com/libusb/libusb/blob/master/COPYING)-licensed library for USB device access from Linux, macOS, Windows and others.
- [copy-partitions-20220613-signed.zip](https://mirrorbits.lineageos.org/tools/copy-partitions-20220613-signed.zip) The copy-partitions script was created by LineageOS developer erfanoabdi and filipepferraz and released under LGPL. It is used when the partitions need to be copied before flashing.


## Acknowledgements

* Funded from September 2022 until February 2023 by ![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)


## License
Original development by [Tobias Sterbak](https://tobiassterbak.com). Copyright (C) 2022-2023.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
