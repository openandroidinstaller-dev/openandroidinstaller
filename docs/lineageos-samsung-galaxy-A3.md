# Install LineageOS on Samsung Galaxy A3 (2017)

## Unlock the bootloader
- https://www.hardreset.info/devices/samsung/samsung-galaxy-a3-core/faq/bootloader-unlock/samsung-bootloader/ (Methode 2)

- enter download mode:
    - `adb reboot download` (https://www.thecustomdroid.com/samsung-galaxy-download-odin-mode-guide)
- enter bootloader samsung:
    - `adb reboot recovery` (https://technastic.com/samsung-recovery-mode/)
- go into fastboot mode: 
    - https://www.hardreset.info/devices/samsung/samsung-galaxy-a3-core/fastboot-mode/
    - https://www.tenorshare.com/fix-android/how-to-enter-fastboot-mode-on-samsung.html (buttons worked)


## Heimdall
- download heimdall: https://androidfilehost.com/?w=files&flid=304516
- install heimdall: 
    $ unzip /path/to/heimdall_ubuntu.zip -d /tmp
    $ cp /tmp/bin/heimdall* /usr/bin/
    $ rm -rf /tmp/bin


## Files
- TWRP: https://eu.dl.twrp.me/a3y17lte/twrp-3.6.2_9-0-a3y17lte.img.html
- LineageOS: https://firmware.jpod.cc/lineageos/16.0/external/mcfy.fr/a3y17lte/

## Restore vendor image
- stock firmware: 
    - download: https://sfirmware.com/samsung-sm-a320fl/ --> Download the file for firmware version A320FLXXS9CTK2
        - download the file, extract the zip and tars, then move all files to common folder, extract the lz4 with `unlz4 -m *.lz4`
    - manual: https://forum.xda-developers.com/t/guide-installing-stock-firmware-with-heimdall-on-tab-s2-t710.4087141/
    - steps:
        1. Extract all the files from the from the Heimdall zip you download
        2. Execute Heimdall-frontend.exe on Windows, the Heimdall executable on Mac OS or on your Linux terminal, type "heimdall-frontend"
        3. Put your device into download mode.
        4. Plug your device into your computer. If you go to the "Utilities" tab and press the "Detect Device" Button. If it has been detected, you can continue on.
        5. Go on the "Flash" tab. From then, you need to take up a .pit file that has been saved into your computer.
        6. After taking your .pit file, you'll need to add a partition. Then selecting the partition you'll need to flash from the dropdown menu.
        7. Be sure to check carefully each partition so you know that each partition equals their file counterparts.
        8. When that is done, depending on if you're going to stock or not, check the "Repartition" box.
        9. After you've been SURE that ALL those check-ups have been made, press the "Start" button.
        10. Let the program do it's things. Then when it's done, your device should reboot automatically and it's a SUCCESS!!
        Note: DO NOT EVER unplug the cable as the result will probably be a pricey plastic brick in your hands now.
