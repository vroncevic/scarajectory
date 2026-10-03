# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Parameter bundle holding dependencies for TrajectoryCanvas construction.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.trajectory.plan.mutation.iplan_point_mutator import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True)
class CanvasBundle:
    '''
        Immutable container holding dependencies for TrajectoryCanvas.

        It defines:

            :attributes:
                | store - Active waypoint query and storage service.
                | selection - Active waypoint selection coordinator.
                | mutation - Plan point mutator service.
                | dispatcher - Plan mutation observer dispatcher.
                | validator - Kinematic reachability validator.
                | settings - Active canvas parameters and deadzone configuration.
    '''

    store: IWaypointStore
    selection: IPlanSelectionCoordinator
    mutation: IPlanPointMutator
    dispatcher: IPlanObserverDispatcher
    validator: ITrajectoryValidator
    settings: CanvasSettings
