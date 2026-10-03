# -*- coding: UTF-8 -*-

'''
Module
    icanvas_viewport_pan_handler.py
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
    Interface contract for interactive canvas viewport panning handlers.
'''

from __future__ import annotations

from tkinter import Event
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
class ICanvasViewportPanHandler(Protocol):
    '''
        Protocol defining interactive canvas viewport pan translation.

        It defines:

            :methods:
                | try_start_pan - Checks event and initiates viewport pan.
                | pan_drag - Translates viewport offsets during active drag.
                | stop_pan - Terminates active viewport panning on release.
                | is_panning - Queries active panning state.
    '''

    def try_start_pan(self, event: Event) -> bool:
        '''
            Checks event and initiates viewport panning if applicable.

            :param event: Tkinter mouse Event.
            :return: True if panning was initiated, False otherwise.
        '''

    def pan_drag(self, event_x: int, event_y: int) -> bool:
        '''
            Translates viewport offsets during active mouse drag.

            :param event_x: Current mouse X pixel coordinate.
            :param event_y: Current mouse Y pixel coordinate.
            :return: True if viewport offset was modified, False otherwise.
        '''

    def stop_pan(self) -> bool:
        '''
            Terminates active viewport panning on mouse release.

            :return: True if panning was terminated, False if not panning.
        '''

    def is_panning(self) -> bool:
        '''
            Queries active panning state.

            :return: True if currently panning, False otherwise.
        '''
