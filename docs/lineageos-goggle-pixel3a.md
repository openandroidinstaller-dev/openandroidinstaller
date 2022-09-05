# Install lineage OS google pixel 3a

Official lineage os page: https://wiki.lineageos.org/devices/sargo/
Official lineage os images: https://download.lineageos.org/sargo

Steps: https://wiki.lineageos.org/devices/sargo/install

## More details on steps:
- enable developer options in settings
    - Open Settings, and select “About”.
    - Tap on “Build number” seven times.
    - Go back, and select “Developer options”.
    - Scroll down, and check the “Android debugging” or “USB debugging” entry under “Debugging”.
    - when connected to PC, click "allow debugging" on the phone.
- need to enable "OEM unlooking" in setting!


## How to force restart Pixel 3a
There is a chance that your Pixel’s screen might freeze and stop responding to any taps or commands. In such cases, you’ll need to force restart your phone.
- To force reboot, press and hold the power button for 30 seconds or more.
- Release your hold once the logo lights up the screen.


## Vendor image
- factory reset: https://developers.google.com/android/images
- run `adb reboot bootloader`
- then run `sh flash-all.sh` in the unpacked directory.
- lock the bootloader again by running `adb reboot bootloader` and then `fastboot flashing lock`. Follow the instructions on screen.