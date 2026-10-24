# -*- coding: UTF-8 -*-

'''
Module
    ihandler.py
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
    Interface contract for interactive canvas dragging handlers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvasDragHandler(Protocol):
    '''
        Protocol defining interactive canvas drag operations.

        It defines:

            :methods:
                | handle_drag_select - Updates dragged waypoint position during selection drag.
                | handle_drag_freehand - Samples and appends waypoints along freehand motion path.
    '''

    def handle_drag_select(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint position during select tool drag.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :return: Always False (local redraw handled).
        '''

    def handle_drag_freehand(
        self,
        wx: float,
        wy: float,
        settings: CanvasSettings,
    ) -> bool:
        '''
            Samples and appends waypoints along freehand motion path.

            :param wx: World X coordinate.
            :param wy: World Y coordinate.
            :param settings: Active CanvasSettings.
            :return: Always False (local redraw handled).
        '''
