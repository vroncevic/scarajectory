# -*- coding: UTF-8 -*-

'''
Module
    canvas_selection_mouse_handler_test.py
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
    Unit tests for CanvasSelectionMouseHandler waypoint selection component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service_factory import PlanMutationServiceFactory
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_coordinator_factory import PlanSelectionCoordinatorFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory
from scarajectory.infrastructure.gui.canvas.handler.selection.canvas_selection_mouse_handler import CanvasSelectionMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.selection.canvas_selection_mouse_handler_factory import CanvasSelectionMouseHandlerFactory
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasSelectionMouseHandler(TestCase):
    '''
        Test cases for CanvasSelectionMouseHandler waypoint selection logic.

        It defines:

            :methods:
                | setUp - Initializes fixtures for plan, selection, handler.
                | test_handle_select_down_hit - Tests point selection on hit.
                | test_handle_select_down_miss - Tests deselecting on miss.
                | test_handle_select_drag - Tests dragging selected waypoint.
                | test_handle_select_drag_unselected - Tests unselected drag.
                | test_find_hit_index - Tests spatial hit detection query.
                | test_clear_selection - Tests clearing active selection.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for plan, selection, and handler.

            :exceptions: None.
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
        self.vp = ViewportTransform()
        self.state = CanvasInteractionState()
        self.handler: CanvasSelectionMouseHandler = (
            CanvasSelectionMouseHandlerFactory.create(
                self.store,
                self.selection,
                self.mutation,
                self.vp,
                self.state,
            )
        )

    def test_handle_select_down_hit(self) -> None:
        '''
            Tests waypoint selection on hit.

            :exceptions: None.
        '''
        pt = Waypoint(x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0)
        self.mutation.add_point(pt)

        hit_idx: int = self.handler.handle_select_down(10.5, 20.2)
        self.assertEqual(hit_idx, 0)
        self.assertEqual(self.state.dragged_node_idx, 0)
        self.assertEqual(self.selection.selected_index, 0)

    def test_handle_select_down_miss(self) -> None:
        '''
            Tests deselecting on miss.

            :exceptions: None.
        '''
        pt = Waypoint(x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0)
        self.mutation.add_point(pt)

        hit_idx: int = self.handler.handle_select_down(100.0, 200.0)
        self.assertEqual(hit_idx, -1)
        self.assertEqual(self.state.dragged_node_idx, -1)
        self.assertEqual(self.selection.selected_index, -1)

    def test_handle_select_drag(self) -> None:
        '''
            Tests dragging selected waypoint.

            :exceptions: None.
        '''
        pt = Waypoint(x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0)
        self.mutation.add_point(pt)
        self.handler.handle_select_down(10.0, 20.0)

        redraw: bool = self.handler.handle_select_drag(55.0, 65.0)
        self.assertFalse(redraw)
        updated: Waypoint = self.store.waypoints[0]
        self.assertEqual(updated.x, 55.0)
        self.assertEqual(updated.y, 65.0)

    def test_handle_select_drag_unselected(self) -> None:
        '''
            Tests unselected drag.

            :exceptions: None.
        '''
        pt = Waypoint(x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0)
        self.mutation.add_point(pt)
        self.state.dragged_node_idx = -1

        redraw: bool = self.handler.handle_select_drag(55.0, 65.0)
        self.assertFalse(redraw)
        unchanged: Waypoint = self.store.waypoints[0]
        self.assertEqual(unchanged.x, 10.0)
        self.assertEqual(unchanged.y, 20.0)

    def test_find_hit_index(self) -> None:
        '''
            Tests spatial hit detection query.

            :exceptions: None.
        '''
        pt1 = Waypoint(x=0.0, y=0.0, z=10.0, phi=0.0, speed=20.0)
        pt2 = Waypoint(x=50.0, y=50.0, z=10.0, phi=0.0, speed=20.0)
        self.mutation.add_point(pt1)
        self.mutation.add_point(pt2)

        self.assertEqual(self.handler.find_hit_index(0.5, 0.5), 0)
        self.assertEqual(self.handler.find_hit_index(49.5, 50.2), 1)
        self.assertEqual(self.handler.find_hit_index(100.0, 100.0), -1)

    def test_clear_selection(self) -> None:
        '''
            Tests clearing active selection.

            :exceptions: None.
        '''
        pt = Waypoint(x=0.0, y=0.0, z=10.0, phi=0.0, speed=20.0)
        self.mutation.add_point(pt)
        self.handler.handle_select_down(0.0, 0.0)
        self.assertEqual(self.selection.selected_index, 0)

        self.handler.clear_selection()
        self.assertEqual(self.selection.selected_index, -1)
        self.assertEqual(self.state.dragged_node_idx, -1)


if __name__ == '__main__':
    main()
