# -*- coding: UTF-8 -*-

'''
Module
    canvas_status_presenter.py
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
    Presents and updates cursor position and zoom status readouts.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter.ttk import Label

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasStatusPresenter:
    '''
        Presents and updates cursor position and zoom status readouts.

        It defines:

            :attributes:
                | _on_status - Callback invoked when status text updates.
            :methods:
                | __init__ - Initializes the status presenter.
                | set_hover_label - Configures status bar label for readouts.
                | update_cursor_status - Updates cursor status readout text.
                | clear_status - Clears cursor status readout text.
    '''

    _on_status: Callable[[str], None]

    def __init__(self) -> None:
        '''
            Initializes the status presenter with a no-op handler.

            :exceptions: None.
        '''
        self._on_status = lambda _text: None

    def set_hover_label(self, label: Label) -> None:
        '''
            Configures status bar label for cursor readouts.

            :param label: Tkinter Label widget.
            :exceptions: None.
        '''
        self._on_status = lambda text: label.config(text=text)

    def update_cursor_status(self, text: str) -> None:
        '''
            Updates cursor status readout text.

            :param text: Formatted status text string.
            :exceptions: None.
        '''
        self._on_status(text)

    def clear_status(self) -> None:
        '''
            Clears cursor status readout text.

            :exceptions: None.
        '''
        self._on_status('')
