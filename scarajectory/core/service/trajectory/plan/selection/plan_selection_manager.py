# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_manager.py
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
    Concrete implementation of trajectory waypoint selection state manager.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.plan.selection.iplan_selection_navigator import IPlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_state import IPlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanSelectionManager:
    '''
        Concrete implementation of trajectory waypoint selection state manager composing state and navigator.

        It defines:

            :attributes:
                | _state - Injected collaborator storing and validating selected index.
                | _navigator - Injected collaborator executing navigation operations.
            :methods:
                | __init__ - Initializes selection manager with injected collaborators.
                | selected_index - Returns currently selected waypoint index.
                | set_selected_index - Sets selection index if within valid bounds.
                | select_index - Sets selection index directly.
                | select_last - Selects the last element based on total count.
                | select_first_or_none - Selects first element or -1 if empty.
                | clamp_to_count - Clamps selection to valid range for given count.
                | reset - Clears selection back to -1.
    '''

    _state: IPlanSelectionState
    _navigator: IPlanSelectionNavigator

    def __init__(
        self,
        state: IPlanSelectionState,
        navigator: IPlanSelectionNavigator,
    ) -> None:
        '''
            Initializes selection manager with injected collaborators.

            :param state: Injected IPlanSelectionState instance.
            :param navigator: Injected IPlanSelectionNavigator instance.
            :exceptions: None.
        '''
        self._state: Final[IPlanSelectionState] = state
        self._navigator: Final[IPlanSelectionNavigator] = navigator

    @property
    def selected_index(self) -> int:
        '''
            Returns currently selected waypoint index.

            :return: Selected waypoint index or -1.
            :exceptions: None.
        '''
        return self._state.selected_index

    def set_selected_index(self, index: int, total_count: int) -> bool:
        '''
            Sets selection index if within valid bounds.

            :param index: Target index (-1 to total_count - 1).
            :param total_count: Total count of waypoints.
            :return: True if index is within valid bounds, False otherwise.
            :exceptions: None.
        '''
        return self._state.set_selected_index(index, total_count)

    def select_index(self, index: int) -> None:
        '''
            Sets selection index directly.

            :param index: Target index.
            :exceptions: None.
        '''
        self._navigator.select_index(index)

    def select_last(self, total_count: int) -> None:
        '''
            Selects the last element based on total count.

            :param total_count: Total count of waypoints.
            :exceptions: None.
        '''
        self._navigator.select_last(total_count)

    def select_first_or_none(self, total_count: int) -> None:
        '''
            Selects first element (0) or -1 if empty.

            :param total_count: Total count of waypoints.
            :exceptions: None.
        '''
        self._navigator.select_first_or_none(total_count)

    def clamp_to_count(self, total_count: int) -> None:
        '''
            Clamps selection to valid range for given count.

            :param total_count: Total count of waypoints.
            :exceptions: None.
        '''
        self._state.clamp_to_count(total_count)

    def set_index_direct(self, index: int) -> None:
        '''
            Sets selection index directly without validation.

            :param index: Target index.
            :exceptions: None.
        '''
        self._state.set_index_direct(index)

    def reset(self) -> None:
        '''
            Clears selection back to -1.

            :exceptions: None.
        '''
        self._navigator.reset()
