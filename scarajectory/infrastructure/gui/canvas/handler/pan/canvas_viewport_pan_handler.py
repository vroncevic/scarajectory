# -*- coding: UTF-8 -*-

'''
Module
    canvas_viewport_pan_handler.py
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
    Dedicated handler translating mouse pan events into canvas viewport
    offsets.
'''

from __future__ import annotations

from tkinter import Event
from typing import Final

from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewportPanHandler:
    '''
        Handles mouse button press, drag, and release for viewport panning.

        It defines:

            :attributes:
                | _vp - Viewport transformation matrix.
                | _state - Interactive mouse pan, drag, and selection state.
            :methods:
                | __init__ - Initializes pan handler with viewport and state.
                | try_start_pan - Checks event and initiates viewport panning.
                | pan_drag - Translates viewport offsets during active drag.
                | stop_pan - Terminates active viewport panning on release.
                | is_panning - Queries active panning state.
    '''

    _vp: ViewportTransform
    _state: CanvasInteractionState

    def __init__(
        self,
        vp: ViewportTransform,
        state: CanvasInteractionState,
    ) -> None:
        '''
            Initializes pan handler with viewport and interaction state.

            :param vp: ViewportTransform instance.
            :param state: CanvasInteractionState instance.
            :exceptions: None.
        '''
        self._vp: Final[ViewportTransform] = vp
        self._state: Final[CanvasInteractionState] = state

    def try_start_pan(self, event: Event) -> bool:
        '''
            Checks event and initiates panning if button 2 or 3 is pressed.

            :param event: Tkinter mouse Event.
            :return: True if panning was initiated, False otherwise.
            :exceptions: None.
        '''
        if getattr(event, 'num', 1) in (2, 3):
            self._state.pan_x = event.x
            self._state.pan_y = event.y
            self._state.is_panning = True

            return True

        return False

    def pan_drag(self, event_x: int, event_y: int) -> bool:
        '''
            Translates viewport offsets during active mouse drag.

            :param event_x: Current mouse X pixel coordinate.
            :param event_y: Current mouse Y pixel coordinate.
            :return: True if viewport offset was modified, False otherwise.
            :exceptions: None.
        '''
        if self._state.is_panning:
            self._vp.pan_x += event_x - self._state.pan_x
            self._vp.pan_y += event_y - self._state.pan_y
            self._state.pan_x = event_x
            self._state.pan_y = event_y

            return True

        return False

    def stop_pan(self) -> bool:
        '''
            Terminates active viewport panning on mouse release.

            :return: True if panning was terminated, False if not panning.
            :exceptions: None.
        '''
        if self._state.is_panning:
            self._state.is_panning = False

            return True

        return False

    def is_panning(self) -> bool:
        '''
            Queries active panning state.

            :return: True if currently panning, False otherwise.
            :exceptions: None.
        '''
        return self._state.is_panning
