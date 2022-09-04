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
- stock firmware: 
    - download: https://galaxyfirmware.com/model/SM-A320FL/DBT/A320FLXXU1AQA6
    - manual: https://forum.xda-developers.com/t/guide-installing-stock-firmware-with-heimdall-on-tab-s2-t710.4087141/