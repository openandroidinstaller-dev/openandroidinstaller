# Install LineageOS on Samsung Galaxy A3

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
