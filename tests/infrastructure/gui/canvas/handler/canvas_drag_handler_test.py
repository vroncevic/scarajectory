# -*- coding: UTF-8 -*-

'''
Module
    canvas_drag_handler_test.py
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
    Unit tests for CanvasDragHandler dragging motion component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.service.trajectory.discretization.shape_discretizer_factory import ShapeDiscretizerFactory
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service import PlanMutationService
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service_factory import PlanMutationServiceFactory
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator import PlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator_factory import PlanSelectionCoordinatorFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.store.waypoint_store import WaypointStore
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory
from scarajectory.infrastructure.gui.canvas.handler.canvas_drag_handler import CanvasDragHandler
from scarajectory.infrastructure.gui.canvas.handler.canvas_shape_handler import CanvasShapeHandler
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasDragHandler(TestCase):
    '''
        Test cases for CanvasDragHandler dragging motion logic.

        It defines:

            :methods:
                | setUp - Initializes fixtures for store, mutation, shape handler, and drag handler.
                | test_drag_select_updates_point - Tests updating waypoint location during select drag.
                | test_drag_select_ignores_when_no_node_selected - Tests select drag when no node is dragged.
                | test_drag_freehand_appends_when_threshold_met - Tests appending point during freehand drag.
                | test_drag_freehand_ignores_below_threshold - Tests ignoring freehand point below distance threshold.
    '''

    store: WaypointStore
    selection: PlanSelectionCoordinator
    mutation: PlanMutationService
    state: CanvasInteractionState
    settings: CanvasSettings
    drag_handler: CanvasDragHandler

    def setUp(self) -> None:
        '''
            Initializes fixtures for store, mutation, shape handler, and drag handler.
        '''
        self.store = WaypointStoreFactory.create()
        history = PlanHistoryFactory.create()
        selection_mgr = PlanSelectionManagerFactory.create()
        dispatcher = PlanObserverDispatcherFactory.create()
        self.selection = PlanSelectionCoordinatorFactory.create(
            store=self.store,
            selection=selection_mgr,
            dispatcher=dispatcher,
        )
        self.mutation = PlanMutationServiceFactory.create(
            store=self.store,
            history=history,
            selection=selection_mgr,
            dispatcher=dispatcher,
        )
        self.state = CanvasInteractionState()
        self.settings = CanvasSettings(default_z=10.0, default_speed=25.0)
        discretizer = ShapeDiscretizerFactory.create()
        shape_handler = CanvasShapeHandler(
            plan=self.mutation, discretizer=discretizer
        )
        self.drag_handler = CanvasDragHandler(
            store=self.store,
            mutation=self.mutation,
            state=self.state,
            shape_handler=shape_handler,
        )

    def test_drag_select_updates_point(self) -> None:
        '''
            Tests updating waypoint location during select drag.
        '''
        pt = Waypoint(x=10.0, y=10.0, z=5.0, phi=0.0, speed=15.0)
        self.mutation.add_point(pt)
        self.state.dragged_node_idx = 0

        redraw = self.drag_handler.handle_drag_select(wx=50.0, wy=60.0)
        self.assertFalse(redraw)
        updated_pt = self.store.waypoints[0]
        self.assertEqual(updated_pt.x, 50.0)
        self.assertEqual(updated_pt.y, 60.0)

    def test_drag_select_ignores_when_no_node_selected(self) -> None:
        '''
            Tests select drag when no node is dragged.
        '''
        pt = Waypoint(x=10.0, y=10.0, z=5.0, phi=0.0, speed=15.0)
        self.mutation.add_point(pt)
        self.state.dragged_node_idx = -1

        redraw = self.drag_handler.handle_drag_select(wx=50.0, wy=60.0)
        self.assertFalse(redraw)
        self.assertEqual(self.store.waypoints[0].x, 10.0)

    def test_drag_freehand_appends_when_threshold_met(self) -> None:
        '''
            Tests appending point during freehand drag when distance threshold is met.
        '''
        pt = Waypoint(x=0.0, y=0.0, z=10.0, phi=0.0, speed=25.0)
        self.mutation.add_point(pt)

        # Distance is 10.0 mm > FREEHAND_MIN_DISTANCE_MM (5.0 mm)
        redraw = self.drag_handler.handle_drag_freehand(
            wx=10.0, wy=0.0, settings=self.settings
        )
        self.assertFalse(redraw)
        self.assertEqual(self.store.count, 2)
        self.assertEqual(self.store.waypoints[1].x, 10.0)

    def test_drag_freehand_ignores_below_threshold(self) -> None:
        '''
            Tests ignoring freehand point below distance threshold.
        '''
        pt = Waypoint(x=0.0, y=0.0, z=10.0, phi=0.0, speed=25.0)
        self.mutation.add_point(pt)

        # Distance is 1.0 mm < FREEHAND_MIN_DISTANCE_MM (5.0 mm)
        redraw = self.drag_handler.handle_drag_freehand(
            wx=1.0, wy=0.0, settings=self.settings
        )
        self.assertFalse(redraw)
        self.assertEqual(self.store.count, 1)


if __name__ == '__main__':
    main()
