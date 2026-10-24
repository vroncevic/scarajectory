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
    Unit tests for CanvasBundle data container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.mutation.bulk_mutation.ibulk_mutation import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.mutation.provides import MutationProvides
from scarajectory.core.service.trajectory.plan.observer.idispatcher import IPlanObserverDispatcher
from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.adapter_bundle import CanvasAdapterBundle
from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasBundleTest(TestCase):
    '''
        Test suite verifying CanvasBundle initialization and fields.

        It defines:

            :methods:
                | test_bundle_creation - Verifies CanvasBundle fields and properties.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies CanvasBundle stores and exposes all injected collaborator fields.

            :exceptions: None.
        '''
        store = MagicMock(spec=IWaypointStore)
        selection = MagicMock(spec=IPlanSelectionCoordinator)
        mutation = MagicMock(spec=IPlanPointMutator)
        bulk_mutator = MagicMock(spec=IPlanBulkMutator)
        mutations = MutationProvides(
            plan_point_mutator=mutation,
            plan_bulk_mutator=bulk_mutator,
        )
        dispatcher = MagicMock(spec=IPlanObserverDispatcher)
        validator = MagicMock(spec=ITrajectoryValidator)
        settings = MagicMock(spec=CanvasSettings)
        avoidance = MagicMock(spec=IDeadZoneAvoidanceAdapter)
        planner = MagicMock(spec=IShapePlannerAdapter)
        boundary = MagicMock(spec=IWorkspaceBoundaryAdapter)
        adapters = CanvasAdapterBundle(
            avoidance=avoidance,
            planner=planner,
            boundary=boundary,
        )

        bundle = CanvasBundle(
            store=store,
            selection=selection,
            mutations=mutations,
            dispatcher=dispatcher,
            validator=validator,
            settings=settings,
            adapters=adapters,
        )

        self.assertIs(bundle.store, store)
        self.assertIs(bundle.selection, selection)
        self.assertIs(bundle.mutations, mutations)
        self.assertIs(bundle.mutation, mutation)
        self.assertIs(bundle.bulk_mutator, bulk_mutator)
        self.assertIs(bundle.dispatcher, dispatcher)
        self.assertIs(bundle.validator, validator)
        self.assertIs(bundle.settings, settings)
        self.assertIs(bundle.adapters, adapters)
        self.assertIs(bundle.avoidance_adapter, avoidance)
        self.assertIs(bundle.planner_adapter, planner)
        self.assertIs(bundle.boundary_adapter, boundary)



if __name__ == '__main__':
    main()
