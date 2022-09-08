import chunk
from time import sleep
import flet
from flet import (AppBar, ElevatedButton, Page, Text, View, Row, ProgressRing, Column, FilePicker, FilePickerResultEvent, icons)
from typing import List
from subprocess import check_output, STDOUT, call, CalledProcessError
from functools import partial

from installer_config import InstallerConfig


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
        config_path = "openandroidinstaller/assets/configs/"
        try:
            # read device properties
            output = check_output(["adb", "shell", "dumpsys", "bluetooth_manager", "|", "grep", "\'name:\'", "|", "cut", "-c9-"], stderr=STDOUT).decode() 
            page.views[-1].controls.append(Text(f"Detected: {output}"))
            # load config from file
            config = InstallerConfig.from_file(config_path + output.strip() + ".yaml")
            page.views[-1].controls.append(Text(f"Installer configuration found."))
            page.views[-1].controls.append(ElevatedButton("Confirm and continue", on_click=confirm))
            new_views = views_from_config(config)
            views.extend(new_views)
        except CalledProcessError:
            output = "No device detected!"
            page.views[-1].controls.append(Text(f"{output}"))
        page.update()


    def views_from_config(config: InstallerConfig) -> List[View]:
        new_views = []
        for num_step, step in enumerate(config.steps):
            if step.type == "confirm_button":
                new_views.append(
                    get_new_view(title=step.title, content=[confirm_button(step.content)], index=2+num_step)
                )
            elif step.type == "call_button":
                new_views.append(
                    get_new_view(title=step.title, content=[call_button(step.content, command=step.command)], index=2+num_step)
                )
            elif step.type == "text":
                new_views.append(
                    get_new_view(title=step.title, content=[Text(step.content)], index=2+num_step)
                )
            else:
                raise Exception(f"Unknown step type: {step.type}")
        return new_views
    

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