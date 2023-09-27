#### On unlocking the bootloader

First of all, this tool will not help you bypass any vender locked bootloaders in non-official ways.

Devices by *Samsung, Google, OnePlus, Fairphone* and others make it relatively easy to unlock the bootloader and get good support in the installer.

For some devices, it is necessary to unlock the bootloader manually. You usually need to create an account on the manufacturer's website, wait for a certain time and obtain a code from there. OpenAndroidInstaller will try to guide you as far as possible. These vendors include *Sony, Motorola and Xiaomi* amongst others.

Other phone manufacturers no longer allow you to unlock the bootloader. Nothing can be done if you have not unlocked your device in time. These manufacturers include *Huawei, Honor, LG and ASUS*. Support for these manufacturers will always be very limited.

<details>
    <summary>
        <b>Here is a brief overview of the bootloader policies of some of the most popular brands (may be incomplete/inaccurate)</b>
    </summary>

| Brand | Flashing tool | Unlocking Method | Loss of guarantee\* | Supported models |
|---|---|---|---|---|
| Google | Fastboot | OEM/Flashing unlock | No | Pixel and Nexus |
| Samsung | ODIN or Heimdall | Download mode | **Yes** | Galaxy S and A series<br>(Increasing complexity **on and after S10**) |
| OnePlus | Fastboot | OEM/Flashing unlock | No | All |
| Fairphone | Fastboot | [Code from manufacturer](https://support.fairphone.com/hc/en-us/articles/10492476238865-Manage-the-Bootloader)<br>(**Already unlocked until FP2**) | No | All |
| Xiaomi | Fastboot | [Mi Unlock Tool](https://new.c.mi.com/global/post/101245) | **Yes** | Mi 4c, Redmi Note 3, Mi Note Pro, Redmi 3, Mi 4S, Mi 5 and all devices from 2016 onwards |
| Motorola | Fastboot | [Code from manufacturer](https://en-us.support.motorola.com/app/standalone/bootloader/unlock-your-device-a) | **Yes** | Almost all **except** carrier specific models (e.g. Verizon, AT&T, Tracfone) and certain other models |
| Sony | Fastboot | [Code from manufacturer](https://developer.sony.com/open-source/aosp-on-xperia-open-devices/get-started/unlock-bootloader) | **Yes** | All **except** XQ-CT62 (1Ⅳ US) & XQ-CQ62 (5Ⅳ US) |
| Huawei | Fastboot | No official codes since 2017/2018<br>(**Unofficial methods available**) | **Yes** | Mate 9/9Pro, P10/P10Plus |
| Honor | Fastboot | No official codes since 2017/2018<br>(**Unofficial methods available**) | **Yes** | Honor 8 |
| LG | Fastboot | Impossible since December 2021 | **Yes** |  |
| ASUS | Fastboot | Impossible since May 2023 (ASUS unlocking App) | **Yes** |  |

**\*** In the EU you won't loose your standard 2 years of the warranty when you unlock your bootloader, flash your device or root it. ([source](https://forum.xda-developers.com/t/info-eu-rooting-and-flashing-dont-void-the-warranty.1998801/))

</details>
<br>

You can find more information about the brands and their bootloader policies [here](https://wikilibriste.fr/fr/tutoriels-android/bootloader-unlock) (in French).
