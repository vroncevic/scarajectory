# -*- coding: UTF-8 -*-

'''
Module
    assembler_test.py
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
    Unit tests for PlanPipelineBuilder.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.setup.assembly.plan.assembler import PlanPipelineBuilder
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanPipelineAssemblerTest(TestCase):
    '''
        Tests assembling plan pipeline components via PlanPipelineBuilder.

        It defines:

            :methods:
                | test_build_pipeline - Verifies bundle creation and component presence.
                | test_get_version - Verifies version string.
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
        self.assertIsInstance(bundle.point_mutator, IPlanPointMutator)
        self.assertIsInstance(bundle.bulk_mutator, IPlanBulkMutator)
        self.assertIsInstance(bundle.mutation, IPlanBulkMutator)
        self.assertIsInstance(bundle.history, ITrajectoryPlanHistory)
        self.assertIsInstance(bundle.dispatcher, IPlanObserverDispatcher)

    def test_get_version(self) -> None:
        '''
            Tests assembler version string retrieval.

            :exceptions: None.
        '''
        version: str = PlanPipelineBuilder.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
