### How to contribute your own installation configurations

If you want to use the tool for a non-supported smartphone, the fastest way is to adapt an [existing config file](https://github.com/openandroidinstaller-dev/openandroidinstaller/tree/main/openandroidinstaller/assets/configs). The file should be named after the official `device code` of the device. Add the code output by `adb shell getprop | grep ro.product.device` (when the devices is connected to the computer) as well as the official device code to the `supported_device_codes` list in the config. You can also get the device code by connecting the device to the computer and run OpenAndroidInstaller to detect the device.

**To test your config file with the executable** without using the developer setup, place it in the same directory as the executable. There it will be detected by name. After you created a config file and it works fine, you can open a pull request to make the file available to other users. Please also add the device to the supported devices table above.

#### Content of a config file

A config file consists of two parts. The first part are some metadata about the device and the second parts are the steps to unlock the bootloader, boot a recovery and install the ROMs.

##### How to write Metadata
Every config file should have `metadata` with the following fields:
- `maintainer`: str; Maintainer and author of the config file.
- `device_name`: str; Name of the device.
- `is_ab_device`: bool; A boolean to determine if the device is a/b-partitioned or not.
- `device_code`: str; The official device code.
- `supported_device_codes`: List[str]; A list of supported device codes for the config. The config will be loaded based on this field.
- `twrp-link`: [OPTIONAL] str; name of the corresponding twrp page.

In addition to these metadata, every config can have optional `requirements`. If these are set, the user is asked to check if they are meet.
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
- `img`: [OPTIONAL] Display an image on the left pane of the step view. Images are loaded from `openandroidinstaller/assets/imgs/`.
- `content`: str; The content text displayed alongside the action of the step. Used to inform the user about what's going on. For consistency and better readability the text should be moved into the next line using `>`.
- `link`: [OPTIONAL] Link to use for the link button if type is `link_button_with_confirm`.
- `command`: [ONLY for call_button* steps] str; The command to run. One of `adb_reboot`, `adb_reboot_bootloader`, `adb_reboot_download`, `adb_sideload`, `adb_twrp_wipe_and_install`, `adb_twrp_copy_partitions`, `fastboot_boot_recovery`, `fastboot_unlock_with_code`, `fastboot_unlock`, `fastboot_oem_unlock`, `fastboot_get_unlock_data`, `fastboot_reboot`, `heimdall_flash_recovery`.
- `allow_skip`: [OPTIONAL] boolean; If a skip button should be displayed to allow skipping this step. Can be useful when the bootloader is already unlocked.

**Please try to retain this order of these fields in your config to ensure consistency.**

