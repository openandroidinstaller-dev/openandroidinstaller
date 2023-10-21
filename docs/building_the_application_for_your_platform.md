## How to build the application for your platform

The executables for the OpenAndroidInstaller are build with [pyinstaller](https://pyinstaller.org/en/stable/index.html). You can create builds for MacOS or Linux with `make build-app`. For Windows the paths need to be modified. For now, you can have a look [here](https://github.com/openandroidinstaller-dev/openandroidinstaller/blob/v0.1.2-alpha/.github/workflows/manual-build-windows.yml#L22) on how it's done.

If you build the application for your platform and want to contribute the build, please reach out to me.

## Run OpenAndroidInstaller for development

Currently development is only supported on Ubuntu Linux. MacOS and Windows should also work fine. You might need to install additional USB-drivers on Windows.

1. Clone the main branch of this repository
2. Run `make poetry` and `make install` to install poetry to manage python and install the required dependencies like adb, fastboot and heimdall.
3. Run `make app` to start the desktop app from the source.

