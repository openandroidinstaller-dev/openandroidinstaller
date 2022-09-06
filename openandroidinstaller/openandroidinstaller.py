import flet
from flet import AppBar, ElevatedButton, Page, Text, View, Row


def main(page: Page):
    page.title = "OpenAndroidInstaller"
    views = []    

    # Click-event handlers

    def go_next(e):
        view_num = int(page.views[-1].route) + 1
        if view_num > 6:
            view_num = 6
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

    # Generate the Views for the different steps

    def get_nav() -> Row:
        return Row([
            ElevatedButton("Back", on_click=go_back),
            ElevatedButton("Next", on_click=go_next),
        ])


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
                Text("Turn on developer options and OEM Unlock on your phone."),
                get_nav(),
            ],
        )

    
    def get_image_select_view(page: Page) -> View:
        return View(
            "2",
            [
                AppBar(title=Text("Select images.")),
                get_nav(),
            ],
        )


    def get_recovery_view(page: Page) -> View:
        return View(
            "3",
            [
                AppBar(title=Text("Boot recovery")),
                get_nav(),
            ],
        )

    
    def get_install_view(page: Page) -> View:
        return View(
            "4",
            [
                AppBar(title=Text("Install Lineage OS")),
                get_nav(),
            ],
        )


    def get_success_view(page: Page) -> View:
        return View(
            "5",
            [
                AppBar(title=Text("Success!")),
                ElevatedButton("Back", on_click=go_back),
            ],
        )

    # main part

    views = [
        get_welcome_view(page),
        get_bootloader_view(page),
        get_image_select_view(page),
        get_recovery_view(page),
        get_install_view(page),
        get_success_view(page)
    ]

    page.views.append(views[0])
    page.update()


flet.app(target=main, assets_dir="assets")
