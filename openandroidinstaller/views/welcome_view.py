"""Contains the welcome view."""

# This file is part of OpenAndroidInstaller.
# OpenAndroidInstaller is free software: you can redistribute it and/or modify it under the terms of
# the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.

# OpenAndroidInstaller is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with OpenAndroidInstaller.
# If not, see <https://www.gnu.org/licenses/>."""
# Author: Tobias Sterbak

from typing import Callable

from flet import (
    Divider,
    ElevatedButton,
    Row,
    icons,
)

from styles import (
    Text,
    Markdown,
)

from views import BaseView
from app_state import AppState
from widgets import get_title


class WelcomeView(BaseView):
    def __init__(
        self,
        state: AppState,
        on_confirm: Callable,
    ):
        super().__init__(state=state, image="connect-to-usb.png")
        self.on_confirm = on_confirm

        self.init_visuals()

    def init_visuals(
        self,
    ):
        """Initialize the stateful visual elements of the view."""
        self.continue_button = ElevatedButton(
            "Let's start!",
            on_click=self.on_confirm,
            icon=icons.NEXT_PLAN_OUTLINED,
            disabled=False,
            expand=True,
        )

    def build(self):
        self.clear()

        # build up the main view
        self.right_view_header.controls.extend(
            [get_title("Welcome to the OpenAndroidInstaller!")]
        )
        self.right_view.controls.extend(
            [
                Text(
                    "Great that you want to install alternative, open source Android operating systems!"
                ),
                Text(
                    "We will walk you through the installation process nice and easy."
                ),
                Markdown(
                    """
The following steps are performed in this tool:
- First, we help you to **get your device ready** for the installation process.
- Next, you can **select the operating system** you want to install (with guidance).
- Then, we guide you though the process of **unlocking the bootloader** (if necessary). If you don't know what that means, it will be explained later.
- As a next step, the **operation system is installed**. At this point you can also **select to install additional software** ("addons") like Google Apps.
- Finally your device starts your new operating system.
                """
                ),
                Divider(),
                Markdown(
                    """
Before you continue, make sure
- your devices is on the latest system update.
- you have a backup of all your important data, since this procedure will **erase all data from the phone**.
- to not store the backup on the phone! 

Please note, that vendor specific back-ups will most likely not work on LineageOS!
                """
                ),
                Divider(),
                Row(
                    [
                        self.continue_button,
                    ],
                    alignment="center",
                ),
            ]
        )
        return self.view
