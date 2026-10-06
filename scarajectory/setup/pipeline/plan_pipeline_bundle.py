# -*- coding: UTF-8 -*-

'''
Module
    plan_pipeline_bundle.py
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
    Plan pipeline bundle containing trajectory plan management service interfaces.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class PlanPipelineBundle:
    '''
        Bundle containing trajectory plan management service interfaces.

        It defines:

            :attributes:
                | store - Waypoint storage service interface instance.
                | selection - Plan selection coordinator interface instance.
                | mutation - Plan mutation service interface instance.
                | history - Plan history service interface instance.
                | dispatcher - Plan observer dispatcher interface instance.
    '''

    store: IWaypointStore
    selection: IPlanSelectionCoordinator
    mutation: IPlanMutationService
    history: ITrajectoryHistory
    dispatcher: IPlanObserverDispatcher
