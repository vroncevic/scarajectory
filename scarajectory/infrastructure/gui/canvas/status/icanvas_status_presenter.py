# -*- coding: UTF-8 -*-

'''
Module
    icanvas_status_presenter.py
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
    Defines structural protocol ICanvasStatusPresenter for cursor status.
'''

from __future__ import annotations

from tkinter.ttk import Label
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasStatusPresenter(Protocol):
    '''
        Structural protocol for canvas cursor status presentation.

        It defines:

            :methods:
                | set_hover_label - Configures status bar label for readouts.
                | update_cursor_status - Updates cursor status readout text.
                | clear_status - Clears cursor status readout text.
    '''

    def set_hover_label(self, label: Label) -> None:
        '''
            Configures status bar label for readouts.

            :param label: Tkinter Label widget.
        '''

    def update_cursor_status(self, text: str) -> None:
        '''
            Updates cursor status readout text.

            :param text: Formatted status text string.
        '''

    def clear_status(self) -> None:
        '''
            Clears cursor status readout text.
        '''
