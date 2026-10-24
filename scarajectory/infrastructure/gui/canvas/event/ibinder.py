# -*- coding: UTF-8 -*-

'''
Module
    ibinder.py
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
    Defines structural protocol ICanvasEventBinder for Tk event binding operations.
'''

from __future__ import annotations

from tkinter import Event, Widget
from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasEventBinder(Protocol):
    '''
        Structural protocol defining low-level canvas event binding.

        It defines:

            :methods:
                | bind_events - Registers event listeners on canvas.
                | on_mouse_down - Dispatches mouse click press event.
                | on_mouse_drag - Dispatches mouse drag motion event.
                | on_mouse_up - Dispatches mouse button release event.
                | on_mouse_wheel_or_move - Handles zoom and coordinate readout.
    '''

    def bind_events(self) -> None:
        '''
            Registers event listeners on canvas.
        '''

    def on_mouse_down(self, event: Event[Widget]) -> None:
        '''
            Dispatches mouse click press event.

            :param event: Tkinter Event.
        '''

    def on_mouse_drag(self, event: Event[Widget]) -> None:
        '''
            Dispatches mouse drag motion event.

            :param event: Tkinter Event.
        '''

    def on_mouse_up(self, event: Event[Widget]) -> None:
        '''
            Dispatches mouse button release event.

            :param event: Tkinter Event.
        '''

    def on_mouse_wheel_or_move(self, event: Event[Widget]) -> None:
        '''
            Handles zoom and coordinate readout.

            :param event: Tkinter Event.
        '''
