import chunk
from time import sleep
import flet
from flet import (AppBar, ElevatedButton, Page, Text, View, Row, ProgressRing, Column, FilePicker, FilePickerResultEvent, icons)
from typing import List
from subprocess import check_output, STDOUT, call
from functools import partial


recovery_path = None
image_path = None


def main(page: Page):
    page.title = "OpenAndroidInstaller"
    views = []

    # Click-event handlers

    def confirm(e):
        view_num = int(page.views[-1].route) + 1
        page.views.clear()
        page.views.append(views[view_num])
        page.update()

    def go_back(e):
        view_num = int(page.views[-1].route) - 1
        if view_num < 0:
            view_num = 0
        page.views.clear()
        page.views.append(views[view_num])
        page.update()

    def search_devices(e):
        try:
            output = check_output(["adb", "shell", "dumpsys", "bluetooth_manager", "|", "grep", "\'name:\'", "|", "cut", "-c9-"], stderr=STDOUT).decode() 
            page.views[-1].controls.append(Text(f"Detected: {output}"))
            page.views[-1].controls.append(ElevatedButton("Confirm and continue", on_click=confirm))
            views.extend([
                get_new_view(title="Unlock the bootloader", content=[confirm_button("Turn on developer options and OEM Unlock on your phone.")], index=2),
                get_new_view(title="Boot into recovery", content=[confirm_button("Turn on your device and wait until its fully booted.")], index=3),
                get_new_view(title="Boot into recovery", content=[call_button("Reboot into bootloader", command="adb reboot download")], index=4),
                get_new_view(title="Boot into recovery", content=[call_button("Flash custom recovery", command="heimdall flash --no-reboot --RECOVERY recovery")], index=5),
                get_new_view(title="Boot into recovery", content=[confirm_button("Unplug the USB cable from your device. Manually reboot into recovery. Press the Volume Down + Power buttons for 8~10 seconds until the screen turns black & release the buttons immediately when it does, then boot to recovery with the device powered off, hold Volume Up + Home + Power.")], index=6),
                get_new_view(title="Flash LineageOS", content=[confirm_button("Now tap 'Wipe'. Then tap 'Format Data' and continue with the formatting process. This will remove encryption and delete all files stored in the internal storage.")], index=7),
                get_new_view(title="Flash LineageOS", content=[confirm_button("Return to the previous menu and tap 'Advanced Wipe', then select the 'Cache' and 'System' partitions and then 'Swipe to Wipe'.")], index=8),
                get_new_view(title="Flash LineageOS", content=[confirm_button("On the device, go back and select “Advanced”, “ADB Sideload”, then swipe to begin sideload. Then confirm here")], index=9),
                get_new_view(title="Flash LineageOS", content=[call_button("Flash lineageOS image. Don't remove the USB-Cable!", command="adb sideload image")], index=10),
                get_new_view(title="Boot into recovery", content=[call_button("Reboot into OS", command="adb reboot")], index=11),
                get_new_view(title="Successfully finished flashing", content=[Text("Have fun with LineageOS!")], index=12),
            ])
        except:
            output = "No device detected!"
            page.views[-1].controls.append(Text(f"{output}"))
        page.update()

    def call_to_phone(e, command: str):
        command = command.replace("recovery", recovery_path)
        command = command.replace("image", image_path)
        page.views[-1].controls.append(ProgressRing())
        page.update()
        res = call(f'{command}', shell=True)
        if res != 0:
            page.views[-1].controls.pop()
            page.views[-1].controls.append(Text("Command {command} failed!"))
        else:
            sleep(5)
            page.views[-1].controls.pop()
            page.views[-1].controls.append(ElevatedButton("Confirm and continue", on_click=confirm))
        page.update()

    # file picker setup

    def pick_image_result(e: FilePickerResultEvent):
        selected_image.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        )
        global image_path
        image_path = e.files[0].path
        selected_image.update()

    def pick_recovery_result(e: FilePickerResultEvent):
        selected_recovery.value = (
            ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
        ) 
        global recovery_path
        recovery_path = e.files[0].path
        selected_recovery.update()
            
    pick_image_dialog = FilePicker(on_result=pick_image_result)
    pick_recovery_dialog = FilePicker(on_result=pick_recovery_result)
    selected_image = Text()
    selected_recovery = Text()
    page.overlay.append(pick_image_dialog)
    page.overlay.append(pick_recovery_dialog)

    # Generate the Views for the different steps

    def confirm_button(text: str, confirm_text: str = "Confirm and continue") -> Row:
        words = text.split(" ")
        chunk_size = 10
        if len(words) > chunk_size:
            n_chunks = len(words) // chunk_size
            text_field = [Text(f"{' '.join(words[i*chunk_size:(i+1)*chunk_size])}") for i in range(n_chunks)]
            return Column(text_field + [ElevatedButton(f"{confirm_text}", on_click=confirm)])
        else:
            text_field = Text(f"{text}")
            return Row([text_field, ElevatedButton(f"{confirm_text}", on_click=confirm)])
    
    def call_button(text: str, command: str, confirm_text: str = "Confirm and run") -> Row:
        return Row([
            Text(f"{text}"),
            ElevatedButton(f"{confirm_text}", on_click=partial(call_to_phone, command=command))
        ])

    def get_new_view(title: str, index: int, content: List = []) -> View:
        return View(
            f"{index}", [AppBar(title=Text(f"{title}"))] + content
        )

    # main part

    views = [
        get_new_view(title="Welcome to OpenAndroidInstaller!", content=[ElevatedButton("Search device", on_click=search_devices)], index=0),
        get_new_view(title="Pick image and recovery", content=[Row(
            [
                ElevatedButton(
                    "Pick image file",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_image_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_image,
            ]), Row(
            [
                ElevatedButton(
                    "Pick recovery file",
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_recovery_dialog.pick_files(
                        allow_multiple=False
                    ),
                ),
                selected_recovery,
            ]

        ), confirm_button("Done?")], index=1),
    ]

    page.views.append(views[0])
    page.update()


flet.app(target=main, assets_dir="assets")
