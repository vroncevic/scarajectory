# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_state.py
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
    Concrete implementation of waypoint selection index state and bounds clamping.
'''

from __future__ import annotations

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanSelectionState:
    '''
        Concrete implementation of waypoint selection index state and bounds clamping.

        It defines:

            :attributes:
                | _selected_index - Index of currently selected waypoint.
            :methods:
                | __init__ - Initializes selection state.
                | selected_index - Returns currently selected waypoint index.
                | set_selected_index - Sets selection index if within valid bounds.
                | clamp_to_count - Clamps selection to valid range for given count.
                | set_index_direct - Sets selection index directly without validation.
    '''

    _selected_index: int

    def __init__(self, initial_index: int = -1) -> None:
        '''
            Initializes selection state with optional initial index.

            :param initial_index: Initial selected index (-1 for none).
            :exceptions: None.
        '''
        self._selected_index = initial_index

    @property
    def selected_index(self) -> int:
        '''
            Returns currently selected waypoint index.

            :return: Selected waypoint index or -1.
            :exceptions: None.
        '''
        return self._selected_index

    def set_selected_index(self, index: int, total_count: int) -> bool:
        '''
            Sets selection index if within valid bounds.

            :param index: Target index (-1 to total_count - 1).
            :param total_count: Total count of waypoints.
            :return: True if index is within valid bounds, False otherwise.
            :exceptions: None.
        '''
        if -1 <= index < total_count:
            if self._selected_index == index:
                return False

            self._selected_index = index

            return True

        return False

    def clamp_to_count(self, total_count: int) -> None:
        '''
            Clamps selection to valid range for given count.

            :param total_count: Total count of waypoints.
            :exceptions: None.
        '''
        if self._selected_index >= total_count:
            self._selected_index = total_count - 1

    def set_index_direct(self, index: int) -> None:
        '''
            Sets selection index directly without validation.

            :param index: Target index.
            :exceptions: None.
        '''
        self._selected_index = index
