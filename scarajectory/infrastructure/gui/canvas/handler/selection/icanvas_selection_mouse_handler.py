# -*- coding: UTF-8 -*-

'''
Module
    icanvas_selection_mouse_handler.py
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
    Interface contract for interactive canvas waypoint selection handlers.
'''

from __future__ import annotations

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
class ICanvasSelectionMouseHandler(Protocol):
    '''
        Protocol defining interactive waypoint selection and node dragging.

        It defines:

            :methods:
                | handle_select_down - Processes mouse down for hit detection.
                | handle_select_drag - Updates dragged point during motion.
                | find_hit_index - Computes nearest index within hit radius.
                | clear_selection - Clears active selection and dragged index.
    '''

    def handle_select_down(self, wx: float, wy: float) -> int:
        '''
            Processes mouse down for selection hit detection.

            :param wx: World X coordinate in mm.
            :param wy: World Y coordinate in mm.
            :return: Hit waypoint index, or -1 if no waypoint hit.
        '''

    def handle_select_drag(self, wx: float, wy: float) -> bool:
        '''
            Updates dragged waypoint during selection motion.

            :param wx: World X coordinate in mm.
            :param wy: World Y coordinate in mm.
            :return: True if canvas redraw requested, False otherwise.
        '''

    def find_hit_index(self, wx: float, wy: float) -> int:
        '''
            Computes nearest waypoint index within hit radius.

            :param wx: World X coordinate in mm.
            :param wy: World Y coordinate in mm.
            :return: Hit waypoint index, or -1 if none found.
        '''

    def clear_selection(self) -> None:
        '''
            Clears active selection and dragged index.
        '''
