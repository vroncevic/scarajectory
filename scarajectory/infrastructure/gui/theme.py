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

import tkinter as tk
from tkinter import ttk

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThemeManager:
    '''
        Configures dark theme styles for the Tkinter desktop user interface.

        It defines:

            :methods:
                | apply_theme - Applies dark theme stylesheet and color palette.
    '''

    @classmethod
    def apply_theme(cls, root: tk.Tk) -> None:
        '''
            Applies dark theme stylesheet and color palette.

            :param root: Root Tk application window.
            :exceptions: None.
        '''
        style = ttk.Style(root)
        style.theme_use('clam')

        bg_dark: str = '#1e2227'
        bg_card: str = '#282c34'
        fg_text: str = '#abb2bf'
        accent_blue: str = '#61afef'

        root.configure(bg=bg_dark)
        style.configure('.', background=bg_dark, foreground=fg_text, font=('DejaVu Sans', 9))
        style.configure('TFrame', background=bg_dark)
        style.configure('Card.TFrame', background=bg_card)
        style.configure('TLabel', background=bg_dark, foreground=fg_text, font=('DejaVu Sans', 9))
        style.configure('Header.TLabel', font=('DejaVu Sans', 9, 'bold'), foreground=accent_blue)
        style.configure('TLabelframe', background=bg_dark, foreground=accent_blue)
        style.configure('TLabelframe.Label', background=bg_dark, foreground=accent_blue, font=('DejaVu Sans', 9, 'bold'))

        style.configure('TButton', font=('DejaVu Sans', 9, 'bold'), padding=5, background='#2c313a', foreground=fg_text)
        style.map(
            'TButton',
            background=[('pressed', '#21252b'), ('active', '#3e4451'), ('disabled', '#1e2227')],
            foreground=[('pressed', fg_text), ('active', '#ffffff'), ('disabled', '#5c6370')]
        )

        style.configure('Accent.TButton', background='#3e4451', foreground=accent_blue)
        style.map(
            'Accent.TButton',
            background=[('pressed', '#282c34'), ('active', '#4b5263'), ('disabled', '#21252b')],
            foreground=[('pressed', accent_blue), ('active', '#ffffff'), ('disabled', '#5c6370')]
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

        style.configure('Treeview', background='#181a1f', foreground=fg_text, fieldbackground='#181a1f', rowheight=22)
        style.map('Treeview', background=[('selected', '#3e4451')])
        style.configure('TNotebook', background=bg_dark, borderwidth=0)
        style.configure('TNotebook.Tab', background='#181a1f', foreground='#abb2bf', font=('DejaVu Sans', 9, 'bold'), padding=[14, 6])
        style.map(
            'TNotebook.Tab',
            background=[('selected', '#2c313a'), ('active', '#21252b')],
            foreground=[('selected', '#61afef'), ('active', '#ffffff')]
        )
