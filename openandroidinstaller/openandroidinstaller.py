"""Main file of the OpenAndroidInstaller."""

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

import os
import sys
import webbrowser
from pathlib import Path
from time import sleep
from typing import Callable, Optional

import flet
import regex as re
from app_state import AppState
from flet import (
    AppBar,
    Banner,
    Column,
    Container,
    ElevatedButton,
    FloatingActionButton,
    Icon,
    Image,
    Page,
    ProgressBar,
    Text,
    TextButton,
    UserControl,
    colors,
    icons,
)
from installer_config import Step
from loguru import logger
from views import SelectFilesView, StepView, SuccessView, WelcomeView

# where to write the logs
logger.add("openandroidinstaller.log")

# Toggle to True for development purposes
DEVELOPMENT = False 
DEVELOPMENT_CONFIG = "yuga"  # "a3y17lte"  # "sargo"


PLATFORM = sys.platform
# Define asset paths
CONFIG_PATH = (
    Path(__file__).parent.joinpath(Path(os.sep.join(["assets", "configs"]))).resolve()
)
BIN_PATH = Path(__file__).parent.joinpath(Path("bin")).resolve()


class MainView(UserControl):
    def __init__(self):
        super().__init__()
        self.state = AppState(
            platform=PLATFORM,
            config_path=CONFIG_PATH,
            bin_path=BIN_PATH,
            progressbar=ProgressBar(
                width=600, color="#00d886", bgcolor="#eeeeee", bar_height=16
            ),
            num_steps=2,
            test=DEVELOPMENT,
            test_config=DEVELOPMENT_CONFIG,
        )
        # create the main columns
        self.view = Column(expand=True, width=1200)

        # create default starter views
        welcome = WelcomeView(
            on_confirm=self.confirm,
            state=self.state,
        )
        select_files = SelectFilesView(
            on_confirm=self.confirm,
            state=self.state,
        )
        # ordered to allow for pop
        self.default_views = [select_files, welcome]
        # create the final success view
        self.final_view = SuccessView(state=self.state)

        self.state.default_views = self.default_views
        self.state.final_view = self.final_view

    def build(self):
        self.view.controls.append(self.default_views.pop())
        return self.view

    def confirm(self, e):
        """Confirmation event handler to use in views."""
        # remove all elements from column view
        self.view.controls = []
        # if a config is loaded, display a progress bar
        if self.state.config:
            self.state.increment_progressbar()
        # if there are default views left, display them first
        if self.default_views:
            self.view.controls.append(self.default_views.pop())
        elif self.state.steps:
            self.view.controls.append(
                StepView(
                    step=self.state.steps.pop(0),
                    state=self.state,
                    on_confirm=self.confirm,
                )
            )
        else:
            # display the final view
            self.view.controls.append(self.final_view)
        self.view.update()


def main(page: Page):
    logger.info(f"Running OpenAndroidInstaller on {PLATFORM}")
    # Configure the application base page
    page.title = "OpenAndroidInstaller"
    page.window_height = 780
    page.window_width = int(1.77 * page.window_height)
    page.window_top = 100
    page.window_left = 120
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"

    # header
    page.appbar = AppBar(
        leading=Image(
            src=f"/assets/logo-192x192.png", height=40, width=40, border_radius=40
        ),
        leading_width=56,
        toolbar_height=72,
        elevation=0,
        title=Text("OpenAndroidInstaller alpha version", style="displaySmall"),
        center_title=False,
        bgcolor="#00d886",
        actions=[
            Container(
                content=ElevatedButton(
                    icon=icons.BUG_REPORT_OUTLINED,
                    text="Report a bug",
                    on_click=lambda _: webbrowser.open(
                        "https://github.com/openandroidinstaller-dev/openandroidinstaller/issues"
                    ),
                ),
                padding=15,
                tooltip="Report an issue on github",
            )
        ],
    )

    # display a warnings banner
    def close_banner(e):
        page.banner.open = False
        page.update()

    page.banner = Banner(
        bgcolor=colors.AMBER_100,
        leading=Icon(icons.WARNING_AMBER_ROUNDED, color=colors.AMBER, size=40),
        content=Text(
            "These instructions only work if you follow every section and step precisely. Do not continue after something fails!"
        ),
        actions=[
            TextButton("I understand", on_click=close_banner),
        ],
    )
    page.banner.open = True
    page.update()

    # create application instance
    app = MainView()

    # add a button that restarts the process
    def restart_process(e):
        logger.info("Restarted the process. Reset everything.")
        page.controls.pop()
        app = MainView()
        page.add(app)
        page.update()

    page.floating_action_button = FloatingActionButton(
        text="Restart the process",
        icon=icons.RESTART_ALT_OUTLINED,
        tooltip="You can safely restart if you missed a step or didn't make it.",
        on_click=restart_process,
    )

    # add application's root control to the page
    page.add(app)


flet.app(target=main, assets_dir="assets")
