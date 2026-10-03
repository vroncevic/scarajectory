# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_navigator.py
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
    Coordinates selection navigation heuristics across trajectory waypoints.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.plan.selection.iplan_selection_state import IPlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanSelectionNavigator:
    '''
        Coordinates selection navigation heuristics across trajectory waypoints.

        It defines:

            :attributes:
                | _state - Injected collaborator storing and updating selected index state.
            :methods:
                | __init__ - Initializes selection navigator with state collaborator.
                | select_index - Sets selection index directly.
                | select_last - Selects the last element based on total count.
                | select_first_or_none - Selects first element or deselects if empty.
                | reset - Clears selection back to deselected state.
    '''

    _state: IPlanSelectionState

    def __init__(self, state: IPlanSelectionState) -> None:
        '''
            Initializes selection navigator with state collaborator.

            :param state: Injected IPlanSelectionState instance.
            :exceptions: None.
        '''
        self._state: Final[IPlanSelectionState] = state

    def select_index(self, index: int) -> None:
        '''
            Sets selection index directly.

            :param index: Target index.
            :exceptions: None.
        '''
        self._state.set_index_direct(index)

    def select_last(self, total_count: int) -> None:
        '''
            Selects the last element based on total count.

            :param total_count: Total count of waypoints.
            :exceptions: None.
        '''
        self._state.set_index_direct(total_count - 1)

    def select_first_or_none(self, total_count: int) -> None:
        '''
            Selects first element (0) or -1 if empty.

            :param total_count: Total count of waypoints.
            :exceptions: None.
        '''
        self._state.set_index_direct(0 if total_count > 0 else -1)

    def reset(self) -> None:
        '''
            Clears selection back to deselected state (-1).

            :exceptions: None.
        '''
        self._state.set_index_direct(-1)
