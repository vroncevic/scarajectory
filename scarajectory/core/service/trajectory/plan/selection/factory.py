# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Top-level factory assembling the trajectory plan selection subsystem.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.plan.selection.coordinator.coordinator import PlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.coordinator.dependencies import SelectionCoordinatorDependencies
from scarajectory.core.service.trajectory.plan.selection.coordinator.factory import SelectionCoordinatorFactory
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
from scarajectory.core.service.trajectory.plan.selection.navigator.factory import SelectionNavigatorFactory
from scarajectory.core.service.trajectory.plan.selection.navigator.navigator import PlanSelectionNavigator
from scarajectory.core.service.trajectory.plan.selection.provides import SelectionProvides
from scarajectory.core.service.trajectory.plan.selection.state.factory import SelectionStateFactory
from scarajectory.core.service.trajectory.plan.selection.state.state import PlanSelectionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SelectionFactory:
    '''
        Top-level factory assembling and wiring the selection subsystem.

        It defines:

            :methods:
                | create - Assembles selection subsystem and returns provides container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: SelectionDependencies) -> SelectionProvides:
        '''
            Assembles selection subsystem components and returns SelectionProvides container.

            :param dependencies: Injected SelectionDependencies bundle.
            :return: Fully wired SelectionProvides instance.
            :exceptions: None.
        '''
        state: PlanSelectionState = SelectionStateFactory.create(
            dependencies.initial_index
        )
        navigator: PlanSelectionNavigator = SelectionNavigatorFactory.create(
            state
        )
        coordinator: PlanSelectionCoordinator = (
            SelectionCoordinatorFactory.create(
                SelectionCoordinatorDependencies(
                    waypoint_store=dependencies.waypoint_store,
                    plan_selection_state=state,
                    plan_observer_dispatcher=dependencies.plan_observer_dispatcher,
                )
            )
        )

        return SelectionProvides(
            plan_selection_coordinator=coordinator,
            plan_selection_state=state,
            plan_selection_navigator=navigator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
