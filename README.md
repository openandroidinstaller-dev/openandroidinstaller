<br />
<div align="center">
  <h1>OpenAndroidInstaller</h1>
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
Samsung | Galaxy A5 2016 | a5xelte |  | under development
Google | Pixel 3a | sargo | sargo | tested
Sony | Xperia Z | yuga | C6603 | tested
Sony | Xperia Z3 | z3 | | under development
Sony | Xperia ZX | kagura | | under development
Fairphone | Fairphone 2 | FP2 | | under development


## Usage

Currently, only linux is supported. 

1. Download the AppImage, .exe or appropriate file for your OS. 
2. Download the lineageOS image and the custom recovery image. A source for files can be found here: https://lineageosroms.com
3. Start the desktop app and follow the instructions.


## Run OpenAndroidInstaller for development

Currently development is only supported on Ubunut Linux. MacOS should also work fine.

1. Clone the main branch of this repository
2. Run `make install` to install poetry to manage python and install the requirend dependencies like adb, fastboot and heimdall.
3. Run `make app` to start the desktop app from the source.


## Contributing

### Contribute your own installation configurations

If you want to use the tool for a non-supported smartphone, the fastest way is to adapt an [existing config file](https://github.com/openandroidinstaller-dev/openandroidinstaller/tree/main/openandroidinstaller/assets/configs).

Every step in the config file corresponds to one view in the application. These steps should contain the following fields:
- `title`: str; Describing the overall goal of the step. Will be displayed in the header of the view.
- `type`: str; Corresponds to the type of view to generate. There are the following options:
  - `text`: Just display the text given in content.
  - `confirm_button`: Display the content, as well as a button to allow the user to go to the next step.
  - `call_button`: Display the content text and a button that runs a given command. After the command is run, a confirm button is displayed to allow the user to move to the next step.
  - `call_button_with_input`: Display the content text, an input field and a button that runs a given command. The inputtext, can be used in the command by using the `<inputtext>` placeholder in the command field. After the command is run, a confirm button is displayed to allow the user to move to the next step.
- `content`: str; The content text displayed alongside the action of the step. Used to inform the user about whats going on.
- `command`: [ONLY for call_button* steps] str; This is a terminal command run in a shell. (For example fastboot or adb). There are three types of placeholders supported, that will be filled by the tool as soon as information is given.
  - `<image>`: The path of the image file.
  - `<recovery>`: The path of the recovery file.
  - `<inputtext>`: Text from the user input from `call_button_with_input` views.
- `img`: Display an image on the left pane of the step view. Images are loaded from `openandroidinstaller/assets/imgs/`.
- `allow_skip`: [OPTIONAL] boolean; If a skip button should be displayed to allow skipping this step. Can be useful when the bootloader is already unlocked.

After you created a config file, you can open a pull request to make the file available to other users. The file should be named after device name output by `adb shell dumpsys bluetooth_manager | grep 'name:' | cut -c9-` when the devices is connected to the computer. Please also add the device to the supported devices table above.


## Tools

- The [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools) (such as adb and fastboot) are [Apache](https://android.googlesource.com/platform/system/adb/+/refs/heads/master/NOTICE)-licensed universal Android utilities
- [Heimdall](https://gitlab.com/BenjaminDobell/Heimdall/) is an [MIT](https://gitlab.com/BenjaminDobell/Heimdall/-/blob/master/LICENSE)-licensed replacement for the leaked ODIN tool to flash Samsung devices.


## Acknowledgements

* Funded from September 2022 until February 2023 by ![logos of the "Bundesministerium für Bildung und Forschung", Prodotype Fund and OKFN-Deutschland](resources/pf_funding_logos.svg)


## License
Original development by [Tobias Sterbak](https://tobiassterbak.com). Copyright (C) 2022.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).