<br />
<div align="center">
  <h1>OpenAndroidInstaller</h1>

  [![License](https://img.shields.io/github/license/openandroidinstaller-dev/openandroidinstaller?color=green&style=flat-square)](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/LICENSE)
  [![Release](https://img.shields.io/github/v/release/openandroidinstaller-dev/openandroidinstaller?include_prereleases&style=flat-square)](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases)
  [![Downloads](https://img.shields.io/github/downloads/openandroidinstaller-dev/openandroidinstaller/total?style=flat-square)](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases)
  [![Flathub](https://img.shields.io/flathub/downloads/org.openandroidinstaller.OpenAndroidInstaller?label=flathub%20installs&style=flat-square)](https://flathub.org/apps/org.openandroidinstaller.OpenAndroidInstaller)
  [![Twitter](https://img.shields.io/twitter/follow/oainstaller?style=social)](https://twitter.com/OAInstaller)
  [![Mastodon](https://img.shields.io/mastodon/follow/109341220262803943?domain=https%3A%2F%2Ffosstodon.org&style=social)](https://fosstodon.org/@openandroidinstaller)
  <p>Makes installing alternative Android distributions nice and easy.</p>
  <a href="https://github.com/openandroidinstaller-dev/openandroidinstaller">
    <img src="openandroidinstaller/assets/logo-192x192.png" alt="OpenAndroidInstaller" height="80">
  </a>

  <p align="center">
    <br />
    The OpenAndroidInstaller project helps Android users to keep their smartphone's operating system up to date with free software and to continue using the device even though the manufacturer no longer offers updates. With a graphical installation software, users are easily guided through the installation process of free Android operating systems like <a href="https://lineageos.org">LineageOS</a>.
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

> [!WARNING]
> This application is currently in beta state, so use at your own risk! While many people tested the application so far and we heard of no bricked devices, things might still go wrong.

> [!IMPORTANT]
> Unlocking the bootloader will erase all data on your device!
> This also includes your DRM keys, which are stored in the Trim Area partition (also called TA) in case your device is fairly recent and supports DRM L1. Those devices will be downgraded to DRM L3. Devices on DRM L3 by default will not be affected.
> Before proceeding, ensure the data you would like to retain is backed up to your PC and/or your Google account, or equivalent. Please note that OEM backup solutions like Samsung and Motorola backup may not be accessible from LineageOS once installed.
> If you wish to backup the TA partition first, you can find tutorials related to your device on the internet.

## Usage

Linux is currently the best supported platform (tested with Ubuntu 20.04/22.04 LTS). Windows and MacOS are also supported but you might experience more issues. So far there is no support for ARM-based systems.

1. Download the [.exe or appropriate executable file for your OS](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases) from the releases or get the [official flatpak from flathub](https://flathub.org/apps/org.openandroidinstaller.OpenAndroidInstaller). You might need to change permissions to run the executable.
    - On Windows also [install the Universal USB Drivers](https://adb.clockworkmod.com) and other potentially drivers needed for your device.
2. Download the custom ROM image and the TWRP recovery image for your device and optionally some addons. A source for files can be found on the following websites:
    - some custom ROMs:
      - [LineageOS](https://wiki.lineageos.org/devices)
      - [/e/OS](https://doc.e.foundation/devices)
      - [LineageOS for microg](https://download.lineage.microg.org)
      - [BlissRoms](https://blissroms.org)
      - [PixelExperience](https://download.pixelexperience.org)
    - TWRP Recovery:
      - [TWRP recovery](https://twrp.me/Devices)
    - Optional Addons:
      - There are different packages of *Google Apps* available.
        - [MindTheGapps](https://wiki.lineageos.org/gapps#downloads)
        - [NikGApps](https://nikgapps.com)
      - [MicroG](https://microg.org)
        - The recommended way to install MicroG is to use the zip file provided here: [https://github.com/FriendlyNeighborhoodShane/MinMicroG-abuse-CI/releases](https://github.com/FriendlyNeighborhoodShane/MinMicroG-abuse-CI/releases).
      - [F-Droid App-Store](https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota).
    - or you can just search the web or the [xda-developers forum](https://forum.xda-developers.com) for an appropriate version for your device.
3. Start the desktop app and follow the instructions.


## Officially supported devices

Currently, the **we support 62 devices** by various vendors and working on adding more soon!


Support for these devices is provided as best effort, but things might still go wrong.
Help to improve the tool by reporting any issues you might face.

<details><summary><b>Samsung</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Samsung | Galaxy J7 2015 | j7elte | | tested
Samsung | Galaxy A3 2017 | a3y17lte | SM-A320FL | tested
Samsung | Galaxy A5 2016 | [a5xelte](https://wiki.lineageos.org/devices/a5xelte) | SM-A510F | tested
Samsung | Galaxy A5 2017 | [a5y17lte](https://wiki.lineageos.org/devices/a5y17lte) | | tested
Samsung | Galaxy A7 2016 | a7xelte | | tested
Samsung | Galaxy Grand Prime VE | grandprimevelte | SM-G531F | tested
Samsung | Galaxy S III Neo | s3ve3g | GT-I9301I | tested
Samsung | Galaxy Tab S2 | [gts210vewifi](https://wiki.lineageos.org/devices/gts210vewifi/) | T813 | tested
Samsung | Galaxy S4 Mini LTE| [serranoltexx](https://wiki.lineageos.org/devices/serranoltexx) | | tested
Samsung | Galaxy S5 | [klte](https://wiki.lineageos.org/devices/klte) | G900F/M/R4/R7/T/V/W8 | tested
Samsung | Galaxy S6 | [zerofltexx](https://wiki.lineageos.org/devices/zerofltexx) | | tested
Samsung | Galaxy S6 Edge | [zeroltexx](https://wiki.lineageos.org/devices/zeroltexx) | | tested
Samsung | Galaxy S7 | [herolte](https://wiki.lineageos.org/devices/herolte) | SM-G930F | tested
Samsung | Galaxy S7 Edge | [hero2lte](https://wiki.lineageos.org/devices/hero2lte) | | tested
Samsung | Galaxy S8 | dreamlte | | tested
Samsung | Galaxy S9 | [starlte](https://wiki.lineageos.org/devices/starlte) | | tested
Samsung | Galaxy S10 | [beyond1lte](https://wiki.lineageos.org/devices/beyond1lte) | | tested
Samsung | Galaxy S10e | [beyond0lte](https://wiki.lineageos.org/devices/beyond0lte) | | tested
Samsung | Galaxy S10+ | [beyond2lte](https://wiki.lineageos.org/devices/beyond2lte) | | tested
Samsung | Galaxy Note 3 LTE | [hltetmo](https://wiki.lineageos.org/devices/hltetmo) | N900T/V/W8 | tested
Samsung | Galaxy Note 8 | greatlte | SM-N950F | tested
Samsung | Galaxy Note 9 | [crownlte](https://wiki.lineageos.org/devices/crownlte) | | tested
Samsung | Galaxy Note 10 | [d1](https://wiki.lineageos.org/devices/d1) | | tested
Samsung | Galaxy Note 10+ | [d2s](https://wiki.lineageos.org/devices/d2s) | | tested
</details>

<details><summary><b>Google</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Google | Pixel 2 | [walleye](https://wiki.lineageos.org/devices/walleye) | walleye | tested
Google | Pixel 2 XL | [taimen](https://wiki.lineageos.org/devices/taimen) | taimen | tested
Google | Pixel 3 | [blueline](https://wiki.lineageos.org/devices/blueline) | blueline | tested
Google | Pixel 3 XL | [crosshatch](https://wiki.lineageos.org/devices/crosshatch) | crosshatch | tested
Google | Pixel 3a | [sargo](https://wiki.lineageos.org/devices/sargo) | sargo | tested
Google | Pixel 3a XL | [bonito](https://wiki.lineageos.org/devices/bonito) | bonito | tested
Google | Pixel 4 | [flame](https://wiki.lineageos.org/devices/flame) | flame | tested 
Google | Pixel 4 XL | [coral](https://wiki.lineageos.org/devices/coral) | coral | tested 
Google | Pixel 4a | [sunfish](https://wiki.lineageos.org/devices/sunfish) | sunfish | tested 
Google | Pixel 5 | [redfin](https://wiki.lineageos.org/devices/redfin) | redfin | tested
Google | Pixel 5a | [barbet](https://wiki.lineageos.org/devices/barbet) | barbet | tested
</details>

<details><summary><b>Sony</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Sony | Xperia Z | [yuga](https://wiki.lineageos.org/devices/yuga) | C6603 | tested
Sony | Xperia Z3 | [z3](https://wiki.lineageos.org/devices/z3) | | tested
Sony | Xperia 10 | [kirin](https://wiki.lineageos.org/devices/kirin) | | tested
Sony | Xperia 10 Plus | [mermaid](https://wiki.lineageos.org/devices/mermaid) | | tested
Sony | Xperia XA2 | [pioneer](https://wiki.lineageos.org/devices/pioneer) | | tested
Sony | Xperia XZ2 | [akari](https://wiki.lineageos.org/devices/akari) | | tested
Sony | Xperia XZ3 | [akatsuki](https://wiki.lineageos.org/devices/akatsuki) | | tested
Sony | Xperia ZX | kagura | | planned
</details>

<details><summary><b>Fairphone</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Fairphone | Fairphone 2 | [FP2](https://wiki.lineageos.org/devices/FP2) | | tested
Fairphone | Fairphone 3 | [FP3](https://wiki.lineageos.org/devices/FP3) | | tested
Fairphone | Fairphone 4 | [FP4](https://wiki.lineageos.org/devices/FP4) | | tested
</details>

<details><summary><b>Motorola</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Motorola | moto g5 | [cedric](https://wiki.lineageos.org/devices/cedric) | | tested
Motorola | moto g6 plus | [evert](https://wiki.lineageos.org/devices/evert) | | tested
Motorola | moto g7 power | [ocean](https://wiki.lineageos.org/devices/ocean) | | tested
Motorola | moto g 5G plus / one 5G | [nairo](https://wiki.lineageos.org/devices/nairo) | | tested
Motorola | moto g 5G / one 5G ace | [kiev](https://wiki.lineageos.org/devices/kiev) | | tested
Motorola | edge | [racer](https://wiki.lineageos.org/devices/racer) | | tested
Motorola | moto z | [griffin](https://wiki.lineageos.org/devices/griffin) | | tested
</details>

<details><summary><b>OnePlus</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
OnePlus | One | [bacon](https://wiki.lineageos.org/devices/bacon) | A0001 | tested
OnePlus | 5 | [cheeseburger](https://wiki.lineageos.org/devices/cheeseburger) | | tested
OnePlus | 5T | [dumpling](https://wiki.lineageos.org/devices/dumpling) | | tested
OnePlus | 6 | [enchilada](https://wiki.lineageos.org/devices/enchilada) | | tested
OnePlus | 6T | [fajita](https://wiki.lineageos.org/devices/fajita) | | tested
OnePlus | 7 | [guacamoleb](https://wiki.lineageos.org/devices/guacamoleb) | | tested
OnePlus | 7 Pro | [guacamole](https://wiki.lineageos.org/devices/guacamole) | | tested
OnePlus | 7T | [hotdogb](https://wiki.lineageos.org/devices/hotdogb) | | tested
OnePlus | 7T Pro | [hotdog](https://wiki.lineageos.org/devices/hotdog) | | tested
OnePlus | Nord | [avicii](https://wiki.lineageos.org/devices/avicii) | | tested
OnePlus | Nord N200 | [dre](https://wiki.lineageos.org/devices/dre) | | tested
OnePlus | 9 | lemonade | | under development
</details>

<details><summary><b>Xiaomi</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Xiaomi | Redmi Note 7 | [lavender](https://wiki.lineageos.org/devices/lavender) |  | tested
Xiaomi | Redmi 7A / 8 / 8A / 8A Dual | [Mi439](https://wiki.lineageos.org/devices/Mi439) : pine / olive / olivelite / olivewood | | tested
Xiaomi | Redmi Note 8 / 8T | [ginkgo](https://wiki.lineageos.org/devices/ginkgo) / willow |  | untested
Xiaomi | Redmi 9A / 9C / 9AT / 9i / 9A Sport / 10A / 10A Sport | garden / dandelion / blossom / angelican | | tested
</details>

And more to come!


## Contributing

All kinds of contributions are welcome. These include:
- Fix and improve texts in configs and in the application.
- Test the tool for a supported device.
- Create a config for a new device.
- Test the application on your computer and/or device.
- Contribute an application build for a new platform.
- Add features and/or improve the code base.
- Report bugs.

[How to contribute your own installation configurations](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/docs/how_to_contribute_your_own_installation_configurations.md)

[How to build the application for your platform](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/docs/building_the_application_for_your_platform.md)

[On unlocking the bootloader](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/docs/unlocking_the_bootloader.md)

More details on how to contribute can be found [here](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/CONTRIBUTING.md).
Please have a look before opening an issue or starting to contribute.

A detailed list can be found [here](https://openandroidinstaller.org/#contribute).


## Tools

- The [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) (such as adb and fastboot) are [Apache](https://android.googlesource.com/platform/system/adb/+/refs/heads/master/NOTICE)-licensed universal Android utilities
- [Heimdall](https://gitlab.com/BenjaminDobell/Heimdall) is an [MIT](https://gitlab.com/BenjaminDobell/Heimdall/-/blob/master/LICENSE)-licensed replacement for the leaked ODIN tool to flash Samsung devices.
- [libusb-1.0](https://github.com/libusb/libusb) is a [LGPL-2.1](https://github.com/libusb/libusb/blob/master/COPYING)-licensed library for USB device access from Linux, macOS, Windows and others.
- [copy-partitions-20220613-signed.zip](https://mirrorbits.lineageos.org/tools/copy-partitions-20220613-signed.zip) The copy-partitions script was created by LineageOS developer erfanoabdi and filipepferraz and released under LGPL. It is used when the partitions need to be copied before flashing.


## Acknowledgements

* Funded from September 2022 until February 2023 by ![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)


## License
Original development by [Tobias Sterbak](https://tobiassterbak.com). Copyright (C) 2022-2023.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [http://www.gnu.org/licenses](http://www.gnu.org/licenses).
