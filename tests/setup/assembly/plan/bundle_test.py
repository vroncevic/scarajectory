# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for PlanPipelineBundle data container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.history.ihistory import ITrajectoryPlanHistory
from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.setup.assembly.plan.bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanPipelineBundleTest(TestCase):
    '''
        Test suite verifying PlanPipelineBundle structure.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle with mock components.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies PlanPipelineBundle exposes attributes.

            :exceptions: None.
        '''
        store: MagicMock = MagicMock(spec=IWaypointStore)
        selection: MagicMock = MagicMock(spec=IPlanSelectionCoordinator)
        point_mutator: MagicMock = MagicMock(spec=IPlanPointMutator)
        bulk_mutator: MagicMock = MagicMock(spec=IPlanBulkMutator)
        history: MagicMock = MagicMock(spec=ITrajectoryPlanHistory)
        dispatcher: MagicMock = MagicMock(spec=IPlanObserverDispatcher)

        bundle: PlanPipelineBundle = PlanPipelineBundle(
            store=store,
            selection=selection,
            point_mutator=point_mutator,
            bulk_mutator=bulk_mutator,
            history=history,
            dispatcher=dispatcher,
        )
        self.assertIs(bundle.store, store)
        self.assertIs(bundle.selection, selection)
        self.assertIs(bundle.point_mutator, point_mutator)
        self.assertIs(bundle.bulk_mutator, bulk_mutator)
        self.assertIs(bundle.mutation, bulk_mutator)
        self.assertIs(bundle.history, history)
        self.assertIs(bundle.dispatcher, dispatcher)


if __name__ == '__main__':
    main()
