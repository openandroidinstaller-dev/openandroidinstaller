"""Contains functions and classes to get different elements and widgets of the installer."""
from functools import partial
from os import path
from typing import Callable

from flet import (Column, Container, ElevatedButton, Image, Row, Text,
                  alignment, icons)


def get_title(title: str):
    image_path = path.abspath(
        path.join(path.dirname(__file__), "assets/logo-192x192.png")
    )
    return Container(
        content=Row(
            [
                Image(src=image_path, height=40, width=40, border_radius=40),
                Text(f"{title}", style="titleMedium"),
            ]
        ),
        margin=0,
        padding=0,
        alignment=alignment.center,
        width=400,
        height=50,
        border_radius=1,
    )


def confirm_button(
    text: str, confirm_func: Callable, confirm_text: str = "Confirm and continue"
) -> Column:
    return Column(
        [
            Text(f"{text}"),
            ElevatedButton(
                f"{confirm_text}",
                on_click=confirm_func,
                icon=icons.NEXT_PLAN_OUTLINED,
            ),
        ],
        horizontal_alignment="center",
    )


def call_button(
    text: str, call_func: Callable, command: str, confirm_text: str = "Confirm and run"
) -> Column:
    return Column(
        [
            Text(f"{text}"),
            ElevatedButton(
                f"{confirm_text}", on_click=partial(call_func, command=command)
            ),
        ],
        horizontal_alignment="center",
    )
