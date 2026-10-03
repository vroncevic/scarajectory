# -*- coding: UTF-8 -*-

'''
Module
    theme_notebook_styler.py
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
    Dedicated notebook tab style configurator for Tkinter TTK Notebook widgets.
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


class ThemeNotebookStyler:
    '''
        Configures notebook container and tab styles on ttk.Style.

        It defines:

            :methods:
                | configure - Applies notebook tabbed container styles to ttk.Style.
    '''

    @classmethod
    def configure(cls, style: Style, palette: dict[str, str]) -> None:
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
