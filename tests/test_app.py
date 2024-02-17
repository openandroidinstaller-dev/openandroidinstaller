"""Test if the main app starts up."""
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
import flet as ft

from openandroidinstaller.openandroidinstaller import main


class MockResult:
    def __init__(
        self,
    ):
        self.results = "testtesttest"


class MockConn:
    def __init__(self):
        self.page_name = "Test page"
        self.pubsubhub = "Pub"

    def send_commands(self, command, other):
        return MockResult()


def test_app_sargo():
    page = ft.Page(conn=MockConn(), session_id=1)
    # test if it would start up
    main(page=page, test=True, test_config="sargo")

    # test if you can go through all views
    state = page.controls[0].state
    state.load_config(device_code="sargo")
    state.default_views.extend(state.addon_views)
    number_of_steps = 14
    for _ in range(number_of_steps):
        page.controls[0].to_next_view(None)
    assert "Installation completed successfully!" in str(
        page.controls[0]
        .view.controls[0]
        .right_view_header.controls[0]
        .content.controls[0]
    )


def test_app_beyond2lte():
    page = ft.Page(conn=MockConn(), session_id=1)
    # test if it would start up
    main(page=page, test=True, test_config="beyond2lte")

    # test if you can go through all views
    state = page.controls[0].state
    state.load_config(device_code="sargo")
    state.default_views.extend(state.addon_views)
    number_of_steps = 14
    for _ in range(number_of_steps):
        page.controls[0].to_next_view(None)
    assert "Installation completed successfully!" in str(
        page.controls[0]
        .view.controls[0]
        .right_view_header.controls[0]
        .content.controls[0]
    )
