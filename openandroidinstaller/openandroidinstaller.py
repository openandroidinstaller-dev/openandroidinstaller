import flet
from flet import AppBar, ElevatedButton, Page, Text, View, colors, FloatingActionButton


def main(page: Page):
    page.title = "OpenAndroidInstaller"
    views = []    


    def go_next(e):
        view_num = int(page.views[-1].route) + 1
        if view_num > 3:
            view_num = 3
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


    def get_welcome_view(page: Page) -> View:
        return View(
            "0",
            [
                AppBar(title=Text("Welcome to OpenAndroidInstaller!")),
                ElevatedButton("Next", on_click=go_next),
            ],
        )

    def get_bootloader_view(page: Page) -> View:
        return View(
            "1",
            [
                AppBar(title=Text("Unlock bootloder")),
                ElevatedButton("Next", on_click=go_next),
                ElevatedButton("Back", on_click=go_back),
            ],
        )

    
    def get_image_select_view(page: Page) -> View:
        return View(
            "2",
            [
                AppBar(title=Text("Select images.")),
                ElevatedButton("Next", on_click=go_next),
                ElevatedButton("Back", on_click=go_back),
            ],
        )


    def get_recovery_view(page: Page) -> View:
        return View(
            "3",
            [
                AppBar(title=Text("Boot recovery")),
                ElevatedButton("Next", on_click=go_next),
                ElevatedButton("Back", on_click=go_back),
            ],
        )

    views = [
        get_welcome_view(page),
        get_bootloader_view(page),
        get_image_select_view(page),
        get_recovery_view(page)
    ]

    page.views.append(views[0])
    page.update()


flet.app(target=main)
