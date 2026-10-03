# -*- coding: UTF-8 -*-

'''
Module
    plan_selection_manager_factory.py
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
    Factory service for creating PlanSelectionManager instances.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager import PlanSelectionManager
from scarajectory.core.service.trajectory.plan.selection.plan_selection_navigator import PlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.plan_selection_state import PlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanSelectionManagerFactory:
    '''
        Factory service for creating PlanSelectionManager instances.

        It defines:

            :methods:
                | create - Instantiates a new PlanSelectionManager.
                | create_with_index - Instantiates a new PlanSelectionManager with initial index.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> PlanSelectionManager:
        '''
            Instantiates a new PlanSelectionManager.

            :return: New PlanSelectionManager instance.
            :exceptions: None.
        '''
        state: PlanSelectionState = PlanSelectionState(-1)
        navigator: PlanSelectionNavigator = PlanSelectionNavigator(state)

        return PlanSelectionManager(state, navigator)

    @classmethod
    def create_with_index(cls, index: int) -> PlanSelectionManager:
        '''
            Instantiates a new PlanSelectionManager with initial index.

            :param index: Initial selected index.
            :return: New PlanSelectionManager instance.
            :exceptions: None.
        '''
        state: PlanSelectionState = PlanSelectionState(index)
        navigator: PlanSelectionNavigator = PlanSelectionNavigator(state)

        return PlanSelectionManager(state, navigator)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
