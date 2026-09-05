# -*- coding: UTF-8 -*-

'''
Module
    theme.py
Copyright
    Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>
    scarajectory is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by the
    Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    scarajectory is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    See the GNU General Public License for more details.
    You should have received a copy of the GNU General Public License along
    with this program. If not, see <http://www.gnu.org/licenses/>.
Info
    Configures modern dark TTK styles and widget palettes for SCARAjectory.
'''

from __future__ import annotations

from tkinter import Tk, ttk
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThemeManager:
    '''
        Configures dark theme styles and design tokens for the Tkinter desktop user interface.

        It defines:

            :attributes:
                | PALETTE - Dictionary of hex color design tokens.
            :methods:
                | get_palette - Returns immutable copy of theme color palette tokens.
                | get_color - Returns color hex value for given design token key.
                | apply_theme - Applies dark theme stylesheet and color palette to root window.
    '''

    PALETTE: ClassVar[dict[str, str]] = {
        'bg_dark': '#1e2227',
        'bg_card': '#282c34',
        'bg_canvas': '#181a1f',
        'fg_text': '#abb2bf',
        'accent_blue': '#61afef',
        'accent_green': '#98c379',
        'accent_red': '#e06c75',
        'accent_yellow': '#e5c07b',
        'border': '#333842'
    }

    @classmethod
    def get_palette(cls) -> dict[str, str]:
        '''
            Returns immutable copy of theme color palette tokens.

            :return: Dictionary mapping color token names to hex color strings.
            :exceptions: None.
        '''
        return cls.PALETTE.copy()

    @classmethod
    def get_color(cls, key: str) -> str:
        '''
            Returns color hex value for given design token key.

            :param key: Design token name (e.g. 'accent_blue', 'bg_dark').
            :return: Hex color string.
            :exceptions: None.
        '''
        return cls.PALETTE.get(key, '#ffffff')

    @classmethod
    def _configure_button_styles(cls, style: ttk.Style, palette: dict[str, str]) -> None:
        '''
            Configures button and accent button pseudo-state styles.

            :param style: Active ttk.Style instance.
            :param palette: Color palette dictionary.
            :exceptions: None.
        '''
        fg: str = palette['fg_text']
        blue: str = palette['accent_blue']

        style.configure('TButton', font=('DejaVu Sans', 9, 'bold'), padding=5, background='#2c313a', foreground=fg)
        style.map(
            'TButton',
            background=[('pressed', '#21252b'), ('active', '#3e4451'), ('disabled', '#1e2227')],
            foreground=[('pressed', fg), ('active', '#ffffff'), ('disabled', '#5c6370')]
        )

        style.configure('Accent.TButton', background='#3e4451', foreground=blue)
        style.map(
            'Accent.TButton',
            background=[('pressed', '#282c34'), ('active', '#4b5263'), ('disabled', '#21252b')],
            foreground=[('pressed', blue), ('active', '#ffffff'), ('disabled', '#5c6370')]
        )

        style.configure('Success.TButton', background='#2e7d32', foreground='#ffffff')
        style.map(
            'Success.TButton',
            background=[('pressed', '#1b5e20'), ('active', '#388e3c'), ('disabled', '#21252b')],
            foreground=[('pressed', '#ffffff'), ('active', '#ffffff'), ('disabled', '#5c6370')]
        )

        style.configure('Danger.TButton', background='#c62828', foreground='#ffffff')
        style.map(
            'Danger.TButton',
            background=[('pressed', '#b71c1c'), ('active', '#e53935'), ('disabled', '#21252b')],
            foreground=[('pressed', '#ffffff'), ('active', '#ffffff'), ('disabled', '#5c6370')]
        )

    @classmethod
    def _configure_notebook_styles(cls, style: ttk.Style, palette: dict[str, str]) -> None:
        '''
            Configures tabbed notebook container styles.

            :param style: Active ttk.Style instance.
            :param palette: Color palette dictionary.
            :exceptions: None.
        '''
        style.configure('TNotebook', background=palette['bg_dark'], borderwidth=0)
        style.configure(
            'TNotebook.Tab',
            background='#181a1f',
            foreground='#abb2bf',
            font=('DejaVu Sans', 9, 'bold'),
            padding=[14, 6],
            focuscolor=palette['bg_dark']
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', '#2c313a'), ('active', '#21252b')],
            foreground=[('selected', palette['accent_blue']), ('active', '#ffffff')]
        )

    @classmethod
    def apply_theme(cls, root: Tk) -> None:
        '''
            Applies dark theme stylesheet and color palette to root window.

            :param root: Root Tk application window.
            :exceptions: None.
        '''
        style = ttk.Style(root)
        style.theme_use('clam')

        palette = cls.get_palette()
        bg_dark: str = palette['bg_dark']
        bg_card: str = palette['bg_card']
        fg_text: str = palette['fg_text']
        accent_blue: str = palette['accent_blue']

        root.configure(bg=bg_dark)
        style.configure('.', background=bg_dark, foreground=fg_text, font=('DejaVu Sans', 9))
        style.configure('TFrame', background=bg_dark)
        style.configure('Card.TFrame', background=bg_card)
        style.configure('TLabel', background=bg_dark, foreground=fg_text, font=('DejaVu Sans', 9))
        style.configure('Header.TLabel', font=('DejaVu Sans', 9, 'bold'), foreground=accent_blue)
        style.configure('TLabelframe', background=bg_dark, foreground=accent_blue)
        style.configure('TLabelframe.Label', background=bg_dark, foreground=accent_blue, font=('DejaVu Sans', 9, 'bold'))

        cls._configure_button_styles(style, palette)
        cls._configure_notebook_styles(style, palette)

        style.configure(
            'Treeview',
            background='#181a1f',
            foreground=fg_text,
            fieldbackground='#181a1f',
            rowheight=22
        )
        style.map('Treeview', background=[('selected', '#3e4451')])
