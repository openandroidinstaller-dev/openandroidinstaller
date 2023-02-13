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
import click
import functools
from pathlib import Path
from typing import List

import flet as ft
from flet import (
    AppBar,
    Banner,
    Column,
    Container,
    ElevatedButton,
    Icon,
    Image,
    Page,
    Text,
    TextButton,
    UserControl,
    colors,
    icons,
)
from loguru import logger

from app_state import AppState
from views import (
    SelectFilesView,
    StepView,
    SuccessView,
    StartView,
    RequirementsView,
    InstallView,
    WelcomeView,
    AddonsView,
    InstallAddonsView,
)
from tooling import run_command

# where to write the logs
logger.add("openandroidinstaller.log")

# VERSION number
VERSION = "0.4.0-beta"

# detect platform
PLATFORM = sys.platform
# Define asset paths
CONFIG_PATH = (
    Path(__file__).parent.joinpath(Path(os.sep.join(["assets", "configs"]))).resolve()
)
BIN_PATH = Path(__file__).parent.joinpath(Path("bin")).resolve()


class MainView(UserControl):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        # create the main columns
        self.view = Column(expand=True, width=1200)

        # create default starter views
        welcome_view = WelcomeView(
            on_confirm=self.to_next_view,
            state=self.state,
        )
        start_view = StartView(
            on_confirm=self.to_next_view,
            on_back=self.to_previous_view,
            state=self.state,
        )
        requirements_view = RequirementsView(
            on_confirm=self.to_next_view,
            on_back=self.to_previous_view,
            state=self.state,
        )
        select_files_view = SelectFilesView(
            on_confirm=self.to_next_view,
            on_back=self.to_previous_view,
            state=self.state,
        )

        # create the install view
        self.install_view = InstallView(on_confirm=self.to_next_view, state=self.state)

        # create the final success view
        self.final_view = SuccessView(state=self.state)

        # initialize the addon view
        self.select_addon_view = AddonsView(
            on_confirm=self.to_next_view, state=self.state
        )
        self.install_addons_view = InstallAddonsView(
            on_confirm=self.to_next_view, state=self.state
        )

        # attach some views to the state to modify and reuse later
        # ordered to allow for pop
        self.state.add_default_views(
            views=[
                select_files_view,
                requirements_view,
                start_view,
                welcome_view,
            ]
        )
        self.state.add_addon_views(
            views=[
                self.install_addons_view,
                self.select_addon_view,
            ]
        )
        # final default views, ordered to allow to pop
        self.state.add_final_default_views(
            views=[
                self.final_view,
                self.install_view,
            ]
        )

        # stack of previous default views for the back-button
        self.previous_views: List = []

    def build(self):
        self.view.controls.append(self.state.default_views.pop())
        return self.view

    def to_previous_view(self, e):
        """Method to display the previous view."""
        # store the current view
        self.state.default_views.append(self.view.controls[-1])
        # clear the current view
        self.view.controls = []
        # retrieve the new view and update
        self.view.controls.append(self.previous_views.pop())
        logger.info("One step back.")
        self.view.update()

    def to_next_view(self, e):
        """Confirmation event handler to use in views."""
        # store the current view
        self.previous_views.append(self.view.controls[-1])
        # remove all elements from column view
        self.view.controls = []
        # if there are default views left, display them first
        if self.state.default_views:
            self.view.controls.append(self.state.default_views.pop())
        elif self.state.steps:
            self.view.controls.append(
                StepView(
                    step=self.state.steps.pop(0),
                    state=self.state,
                    on_confirm=self.to_next_view,
                )
            )
        elif self.state.final_default_views:
            # here we expect the install view to populate the step views again if necessary
            self.view.controls.append(self.state.final_default_views.pop())

        # else:
        #    # display the final view
        #    self.view.controls.append(self.final_view)
        logger.info("Confirmed and moved to next step.")
        self.view.update()


def configure(page: Page):
    """Configure the application."""
    # Configure the application base page
    page.title = "OpenAndroidInstaller"
    page.theme_mode = "light"
    page.window_height = 900
    page.window_width = int(1.5 * page.window_height)
    page.window_top = 100
    page.window_left = 120
    page.scroll = "adaptive"
    page.horizontal_alignment = "center"


def log_version_infos(bin_path):
    """Log the version infos of adb, fastboot and heimdall."""
    # adb
    adbversion = [
        line for line in run_command("adb version", bin_path, enable_logging=False)
    ]
    logger.info(f"{adbversion[1].strip()}")
    # fastboot
    fbversion = [
        line
        for line in run_command("fastboot --version", bin_path, enable_logging=False)
    ]
    logger.info(f"{fbversion[1].strip()}")
    # heimdall
    hdversion = [
        line for line in run_command("heimdall info", bin_path, enable_logging=False)
    ]
    logger.info(f"Heimdall version: {hdversion[1].strip()}")


def main(page: Page, test: bool = False, test_config: str = "sargo"):
    logger.info(f"Running OpenAndroidInstaller version '{VERSION}' on '{PLATFORM}'.")
    log_version_infos(bin_path=BIN_PATH)
    logger.info(100 * "-")

    # configure the page
    configure(page)

    # header
    page.appbar = AppBar(
        leading=Image(
            src="/assets/logo-192x192.png", height=40, width=40, border_radius=40
        ),
        leading_width=56,
        toolbar_height=72,
        elevation=0,
        title=Text(f"OpenAndroidInstaller version {VERSION}", style="displaySmall"),
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

    # create the State object
    state = AppState(
        platform=PLATFORM,
        config_path=CONFIG_PATH,
        bin_path=BIN_PATH,
        test=test,
        test_config=test_config,
    )
    # create application instance
    app = MainView(state=state)

    # add application's root control to the page
    page.add(app)


@click.command()
@click.option(
    "--test", is_flag=True, default=False, help="Start the application in testing mode."
)
@click.option(
    "--test_config", default="sargo", type=str, help="Config to use for testing"
)
def startup(test: bool, test_config: str):
    "Main entrypoint to the app."
    ft.app(
        target=functools.partial(main, test=test, test_config=test_config),
        assets_dir="assets",
    )


if __name__ == "__main__":
    startup()
