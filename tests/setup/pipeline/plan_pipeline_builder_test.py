# -*- coding: UTF-8 -*-

'''
Module
    plan_pipeline_builder_test.py
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
    Unit tests for PlanPipelineBuilder and PlanPipelineBundle.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.plan.mutation.iplan_mutation_service import IPlanMutationService
from scarajectory.core.service.trajectory.plan.observer.iplan_observer_dispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle
from scarajectory.setup.pipeline.plan_pipeline_builder import PlanPipelineBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanPipelineBuilderTestCase(TestCase):
    '''
        Tests assembling plan pipeline components via PlanPipelineBuilder.

        It defines:

            :methods:
                | test_build_pipeline - Verifies bundle creation and component presence.
    '''

    def test_build_pipeline(self) -> None:
        '''
            Tests PlanPipelineBuilder.build assembling PlanPipelineBundle.

            :exceptions: None.
        '''
        bundle: PlanPipelineBundle = PlanPipelineBuilder.build()
        self.assertIsNotNone(bundle)
        self.assertIsInstance(bundle.store, IWaypointStore)
        self.assertIsInstance(bundle.selection, IPlanSelectionCoordinator)
        self.assertIsInstance(bundle.mutation, IPlanMutationService)
        self.assertIsInstance(bundle.history, ITrajectoryHistory)
        self.assertIsInstance(bundle.dispatcher, IPlanObserverDispatcher)


if __name__ == '__main__':
    main()
