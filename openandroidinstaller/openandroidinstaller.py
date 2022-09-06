"""OpenAndroidInstsaller main app."""
from time import sleep
import flet
from flet import Page, Row, TextField, Image, CircleAvatar, Column, ProgressRing
from flet import (ElevatedButton, FilePicker, FilePickerResultEvent, Page, Row, Text, icons)


def main(page: Page):
    # HEADER part
    page.title = "OpenAndroidInstaller"
    page.theme_mode = "dark"
    page.padding = 30
    page.update()

    img = Image(
        src="logo-192x192.png",
        width=100,
        height=100,
        fit="contain",
    )
    page.add(img)

    ### END HEADER

    spinner = Column(
            [ProgressRing(), Text("I'm going to run for ages...")],
            horizontal_alignment="center",
        )
    
    page.add(spinner)

    page.add(
        Row(controls=[
            Text("A"),
            Text("B"),
            Text("C")
        ])
    )

    name_field = TextField(label="Your name")

    def button_clicked(e):
        page.add(Text(f"Your name is {name_field.value}"))

    page.add(
        Row(controls=[
            name_field,
            ElevatedButton(text="Say my name!", on_click=button_clicked)
        ])
    )

flet.app(target=main, assets_dir="assets")