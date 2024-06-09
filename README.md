<div align="center">
  <a href="https://github.com/openandroidinstaller-dev/openandroidinstaller">
    <img src="openandroidinstaller/assets/logo-192x192.png" alt="OpenAndroidInstaller" width="80" height="80">
  </a>

  <h1>OpenAndroidInstaller</h1>
  <p>Makes installing alternative Android distributions nice and easy!</p>

  [![License](https://img.shields.io/github/license/openandroidinstaller-dev/openandroidinstaller?color=green)](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/LICENSE)
  [![Release](https://img.shields.io/github/v/release/openandroidinstaller-dev/openandroidinstaller?include_prereleases)](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases)
  [![Downloads](https://img.shields.io/github/downloads/openandroidinstaller-dev/openandroidinstaller/total)](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases)
  [![Flathub](https://img.shields.io/flathub/downloads/org.openandroidinstaller.OpenAndroidInstaller?label=flathub%20installs)](https://flathub.org/apps/org.openandroidinstaller.OpenAndroidInstaller)
  [![Twitter](https://img.shields.io/twitter/follow/oainstaller?style=social)](https://twitter.com/OAInstaller)
  [![Mastodon](https://img.shields.io/mastodon/follow/109341220262803943?domain=https%3A%2F%2Ffosstodon.org&style=social)](https://fosstodon.org/@openandroidinstaller)

  <p>
    The OpenAndroidInstaller project helps Android users to keep their smartphone's operating system up to date with free software and to continue using the device even though the manufacturer no longer offers updates. With a graphical installation software, users are easily guided through the installation process of free Android operating systems like <a href="https://lineageos.org">LineageOS</a>.
    <br><br>
    <strong>
      <a href="https://openandroidinstaller.org">Website</a>
      ·
      <a href="https://github.com/openandroidinstaller-dev/openandroidinstaller/issues">Report Bugs</a>
      ·
      <a href="mailto: hello@openandroidinstaller.org">Request Feature</a>
    </strong>
  </p>
</div>

> [!WARNING]
> This application is currently in beta state, so use at your own risk! While many people tested the application so far and we heard of no bricked devices, things might still go wrong.

> [!IMPORTANT]
> **Unlocking the bootloader will erase all data on your device!**
> This also includes your DRM keys, which are stored in the Trim Area partition (also called TA) in case your device is fairly recent and supports DRM L1. Those devices will be downgraded to DRM L3. Devices on DRM L3 by default will not be affected.
> Depending on your device you might be able to back up the TA partition using exploits and gaining temporary root access. On Sony Xperia 1/5 series phones DRM L1 will return once the bootloader is relocked.
> Before proceeding, ensure the data you would like to retain is backed up to your PC and/or your Google account, or equivalent. Please note that OEM backup solutions like Samsung and Motorola backup may not be accessible from LineageOS once installed.

## Usage

Linux is currently the best supported platform (tested with Ubuntu 20.04/22.04 LTS). Windows and macOS are also supported, but you might experience more issues.

### 1. Download OpenAndroidInstaller

> [!WARNING]
> ARM-based systems are **not supported**.

OpenAndroidInstaller support all three major operating systems, namely Linux, macOS and Windows.
You can download the correct version for you system from the [GitHub Releases](https://github.com/openandroidinstaller-dev/openandroidinstaller/releases/latest).

The executables are compressed inside `.zip` files, so you'll have to extract them first (make sure you have extracting software installed).
If you get prompted to, you'll have to adjust the permission of the executable to ensure its proper functionality. 

If you run Windows, you might also need to [install the Universal USB Drivers](https://adb.clockworkmod.com) and other potentially drivers needed for your device.

For Linux, a Flatpak version is available in Flathub, [`org.openandroidinstaller.OpenAndroidInstaller`](https://flathub.org/apps/org.openandroidinstaller.OpenAndroidInstaller).

### 2. Download the custom ROM, recovery image & optional add-ons

Here are the official links for:

  - some custom ROMs:
    - [BlissRoms](https://blissroms.org)
    - [CalyxOS](https://calyxos.org)
    - [DivestOS](https://divestos.org)
    - [/e/OS](https://doc.e.foundation/devices)
    - [GrapheneOS](https://grapheneos.org)
    - [LineageOS](https://wiki.lineageos.org/devices)
    - [LineageOS for MicroG](https://download.lineage.microg.org)
    - [PixelExperience](https://download.pixelexperience.org)
  - Recovery:
    - [TWRP recovery](https://twrp.me/Devices)
  - Optional Add-ons:
    - There are different packages of *Google Apps* available:
      - [MindTheGapps](https://wiki.lineageos.org/gapps#downloads)
      - [NikGApps](https://nikgapps.com)
    - [MicroG](https://microg.org)
      - The recommended way to install MicroG is from the `.zip` file provided here: [`MinMicroG-abuse-CI/releases`](https://github.com/FriendlyNeighborhoodShane/MinMicroG-abuse-CI/releases).
    - [F-Droid App-Store](https://f-droid.org/en/packages/org.fdroid.fdroid.privileged.ota).
  - or you can just search the web or the [XDA Developers forum](https://xdaforums.com) to find an appropriate version for your device.

### 3. Start OpenAndroidInstaller

After starting the app you will be prompted to plug your device into your computer and you will be given a step-by-step tutorial on how to install your new OS for your specific device.


## Officially supported devices

Currently, the **we support 88 devices** by various vendors and working on adding more soon!

Support for these devices is provided as best effort, but things might still go wrong.
Help to improve the tool by reporting any issues you might face.


<details><summary><b>Fairphone</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Fairphone | Fairphone 2 | [FP2](https://wiki.lineageos.org/devices/FP2) | | tested
Fairphone | Fairphone 3 | [FP3](https://wiki.lineageos.org/devices/FP3) | | tested
Fairphone | Fairphone 4 | [FP4](https://wiki.lineageos.org/devices/FP4) | | tested

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


<details><summary><b>Motorola</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Motorola | edge | [racer](https://wiki.lineageos.org/devices/racer) | XT2063-2, XT2063-3 | tested
Motorola | moto g5 | [cedric](https://wiki.lineageos.org/devices/cedric) | XT1670, XT1671, XT1672, XT1675, XT1676, XT1677 | tested
Motorola | moto g6 plus | [evert](https://wiki.lineageos.org/devices/evert) | XT1926-2, XT1926-3, XT1926-5, XT1926-6, XT1926-7, XT1926-8, XT1926-9 | tested
Motorola | moto g7 power | [ocean](https://wiki.lineageos.org/devices/ocean) | XT1955-1, XT1955-2, XT1955-4, XT1955-5, XT1955-7 | tested
Motorola | moto g 5G plus / one 5G | [nairo](https://wiki.lineageos.org/devices/nairo) | XT2075-3, XT2075-5 | tested
Motorola | moto g 5G / one 5G ace | [kiev](https://wiki.lineageos.org/devices/kiev) | XT2113-2, XT2113-3 | tested
Motorola | moto z | [griffin](https://wiki.lineageos.org/devices/griffin) | XT1650-3, XT1650-05 | tested

</details>


<details><summary><b>OnePlus</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
OnePlus | One | [bacon](https://wiki.lineageos.org/devices/bacon) | A0001 | tested
OnePlus | 3/3T | [oneplus3](https://wiki.lineageos.org/devices/oneplus3) | A3000, A3003, A3010 | untested
OnePlus | 5 | [cheeseburger](https://wiki.lineageos.org/devices/cheeseburger) | A5000 | tested
OnePlus | 5T | [dumpling](https://wiki.lineageos.org/devices/dumpling) | A5010 | tested
OnePlus | 6 | [enchilada](https://wiki.lineageos.org/devices/enchilada) | A6000, A6003 | tested
OnePlus | 6T | [fajita](https://wiki.lineageos.org/devices/fajita) | A6010, A6013 | tested
OnePlus | 7 | [guacamoleb](https://wiki.lineageos.org/devices/guacamoleb) | GM1900, GM1901, GM1903, GM1905 | tested
OnePlus | 7 Pro | [guacamole](https://wiki.lineageos.org/devices/guacamole) | GM1910, GM1911, GM1913, GM1917 | tested
OnePlus | 7T | [hotdogb](https://wiki.lineageos.org/devices/hotdogb) | HD1900, HD1901, HD1903, HD1905 | tested
OnePlus | 7T Pro | [hotdog](https://wiki.lineageos.org/devices/hotdog) | HD1910, HD1911, HD1913, HD1917 | tested
OnePlus | Nord | [avicii](https://wiki.lineageos.org/devices/avicii) | AC2001, AC2003 | tested
OnePlus | Nord N200 | [dre](https://wiki.lineageos.org/devices/dre) | DE2117 | tested
OnePlus | 9 | lemonade | LE2110, LE2111, LE2113, LE2115 | under development

</details>


<details><summary><b>Samsung</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Samsung | Galaxy J7 2015 | j7elte | | tested
Samsung | Galaxy J7 Prime | on7xelte | | untested
Samsung | Galaxy A3 2017 | a3y17lte | SM-A320FL | tested
Samsung | Galaxy A5 2016 | [a5xelte](https://wiki.lineageos.org/devices/a5xelte) | SM-A510F | tested
Samsung | Galaxy A5 2017 | [a5y17lte](https://wiki.lineageos.org/devices/a5y17lte) | | tested
Samsung | Galaxy A7 2016 | a7xelte | | tested
Samsung | Galaxy A7 2017 | [a7y17lte](https://wiki.lineageos.org/devices/a7y17lte) | | untested
Samsung | Galaxy Grand Prime VE | grandprimevelte | SM-G531F | tested
Samsung | Galaxy S III Neo | s3ve3g | GT-I9301I | tested
Samsung | Galaxy Tab S2 | [gts210vewifi](https://wiki.lineageos.org/devices/gts210vewifi) | T813 | tested
Samsung | Galaxy S4 | [jfltexx](https://wiki.lineageos.org/devices/jfltexx) | | untested
Samsung | Galaxy S4 Mini LTE| [serranoltexx](https://wiki.lineageos.org/devices/serranoltexx) | | tested
Samsung | Galaxy S5 | [klte](https://wiki.lineageos.org/devices/klte) | G900F/M/R4/R7/T/V/W8 | tested
Samsung | Galaxy S5 mini | kminilte | SM-G800F/M/Y | tested
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

<details>
  <summary><b>Sony</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Sony | Xperia Z | [yuga](https://wiki.lineageos.org/devices/yuga) | C6603 | tested
Sony | Xperia Z3 | [z3](https://wiki.lineageos.org/devices/z3) | | tested
Sony | Xperia 10 | [kirin](https://wiki.lineageos.org/devices/kirin) | | tested
Sony | Xperia 10 Plus | [mermaid](https://wiki.lineageos.org/devices/mermaid) | | tested
Sony | Xperia XA2 | [pioneer](https://wiki.lineageos.org/devices/pioneer) | | tested
Sony | Xperia XZ2 | [akari](https://wiki.lineageos.org/devices/akari) | | tested
Sony | Xperia XZ3 | [akatsuki](https://wiki.lineageos.org/devices/akatsuki) | | tested
Sony | Xperia XZ | kagura | | planned

</details>

<details><summary><b>Xiaomi & Poco</b></summary>

Vendor | Device Name | CodeName | Models | Status
---|---|---|---|---
Xiaomi | Redmi 7A / 8 / 8A / 8A Dual | [Mi439](https://wiki.lineageos.org/devices/Mi439) : pine / olive / olivelite / olivewood | | tested
Xiaomi | Redmi 9A / 9C / 9AT / 9i / 9A Sport / 10A / 10A Sport | garden / dandelion / blossom / angelican | | tested
Xiaomi | Redmi 9 / Poco M2 | [lancelot](https://wiki.lineageos.org/devices/lancelot) / galahad / shivan | | untested
Xiaomi | Redmi Note 7 | [lavender](https://wiki.lineageos.org/devices/lavender) |  | tested
Xiaomi | Redmi Note 7 Pro | [violet](https://wiki.lineageos.org/devices/violet) |  | tested
Xiaomi | Redmi Note 8 / 8T | [ginkgo](https://wiki.lineageos.org/devices/ginkgo) / willow |  | untested
Xiaomi | Redmi Note 8 Pro | begonia |  | untested
Xiaomi | Redmi Note 9S / 9 Pro / 9 Pro Max / 10 Lite / Poco M2 pro | [miatoll](https://wiki.lineageos.org/devices/lavender) : gram / curtana / excalibur / joyeuse  |  | untested
Xiaomi | Redmi Note 10S / 11SE / Poco M5S | [rosemary](https://wiki.lineageos.org/devices/rosemary) / maltose / secret /rosemary_p | | untested
Xiaomi | Redmi Note 10 Pro | [sweet](https://wiki.lineageos.org/devices/sweet) | M2101K6G | tested
Xiaomi | Mi A2 / Mi 6X | jasmine_sprout |  | untested
Xiaomi | Mi 8 | [dipper](https://wiki.lineageos.org/devices/dipper) |  | untested
Xiaomi | Mi 9T / Redmi K20 | [davinci](https://wiki.lineageos.org/devices/davinci) / davinciin |  | untested
Xiaomi | Redmi K20 Pro / Mi 9T Pro | raphael / raphaelin | | untested
Xiaomi | Mi 10T / Mi 10T Pro / Redmi K20 | [apollon](https://wiki.lineageos.org/devices/apollon) / apollo |  | untested
Xiaomi | Redmi K40 / Mi 11X / Poco F3 | [alioth](https://wiki.lineageos.org/devices/alioth) / aliothin |  | untested
Xiaomi | Poco X3 / X3 NFC | [surya](https://wiki.lineageos.org/devices/surya) / karna |  | untested
Xiaomi | Poco X3 Pro | [vayu](https://wiki.lineageos.org/devices/vayu) |  | tested
Xiaomi | 12 | cupid | | untested

</details>

... and more to come!

## Tutorials

- Unlocking the bootloader: [`docs/unlocking_the_bootloader.md`](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/docs/unlocking_the_bootloader.md)

- Building the application for your platform: [`docs/building_the_application_for_your_platform.md`](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/docs/building_the_application_for_your_platform.md)

- Contributing your own installation configurations: [`docs/how_to_contribute_your_own_installation_configurations.md`](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/docs/how_to_contribute_your_own_installation_configurations.md)

## Contributing

All kinds of contributions are welcome. These include and are not limited to:

- Fixing and improving texts in configs and in the application
- Testing the tool for a supported device
- Creating a config for a new device
- Testing the application on your computer and/or device
- Contributing an application build for a new platform
- Adding features and/or improving the codebase
- Reporting bugs

Make sure to check if your issue or PR has already been fixed or implemented **before** opening a new one!

### More sources:

- Details on how to contribute: [`CONTRIBUTING.md`](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/main/CONTRIBUTING.md)
- More ways to contribute: [openandroidinstaller.org/#contribute](https://openandroidinstaller.org/#contribute)

## Acknowledgements

* The project received financial support from the German Federal Ministry for Education and Research under the grant identifier 01IS22S26 from September 2022 until February 2023.

![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)

## Credits

- The [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) (such as adb and fastboot) are [Apache](https://android.googlesource.com/platform/system/adb/+/refs/heads/master/NOTICE)-licensed universal Android utilities
- [Heimdall](https://github.com/Benjamin-Dobell/Heimdall) is an [MIT](https://github.com/Benjamin-Dobell/Heimdall/blob/master/LICENSE)-licensed replacement for the leaked ODIN tool to flash Samsung devices.
- [`libusb-1.0`](https://github.com/libusb/libusb) is a [LGPL-2.1](https://github.com/libusb/libusb/blob/master/COPYING)-licensed library for USB device access from Linux, macOS, Windows and others.
- [`copy-partitions-20220613-signed.zip`](https://mirrorbits.lineageos.org/tools/copy-partitions-20220613-signed.zip) The copy-partitions script was created by LineageOS developer erfanoabdi and filipepferraz and released under LGPL. (It's used when the partitions need to be copied before flashing)

## License

Original development by [Tobias Sterbak](https://tobiassterbak.com). Copyright (C) 2022-2024.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [gnu.org/licenses](http://www.gnu.org/licenses).
