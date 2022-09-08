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