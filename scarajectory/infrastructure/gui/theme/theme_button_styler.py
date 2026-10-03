# -*- coding: UTF-8 -*-

'''
Module
    theme_button_styler.py
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
    Dedicated button style configurator for Tkinter TTK themed buttons.
'''

from __future__ import annotations

from tkinter.ttk import Style

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ThemeButtonStyler:
    '''
        Configures button and accent button pseudo-state styles on ttk.Style.

        It defines:

            :methods:
                | configure - Applies button styles and pseudo-states to ttk.Style.
    '''

    @classmethod
    def configure(cls, style: Style, palette: dict[str, str]) -> None:
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
