# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.history.saver.dependencies import PlanHistorySaverDependencies
from scarajectory.core.service.trajectory.history.saver.factory import PlanHistorySaverFactory
from scarajectory.core.service.trajectory.history.stack.factory import PlanHistoryStackFactory
from scarajectory.core.service.trajectory.plan.mutation.dependencies import MutationDependencies
from scarajectory.core.service.trajectory.plan.mutation.factory import MutationFactory
from scarajectory.core.service.trajectory.plan.mutation.point_mutation.ipoint_mutation import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.observer.factory import ObserverFactory
from scarajectory.core.service.trajectory.plan.selection.dependencies import SelectionDependencies
from scarajectory.core.service.trajectory.plan.selection.factory import SelectionFactory
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies
from scarajectory.core.service.trajectory.plan.store.factory import StoreFactory
from scarajectory.infrastructure.gui.canvas.handler.selection.bundle import SelectionHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.selection.handler import CanvasSelectionMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.selection.factory import CanvasSelectionMouseHandlerFactory
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
        self.store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        history_saver = PlanHistorySaverFactory.create(
            PlanHistorySaverDependencies(
                stack=PlanHistoryStackFactory.create()
            )
        )
        dispatcher = ObserverFactory.create().plan_observer_dispatcher
        selection_provides = SelectionFactory.create(
            SelectionDependencies(
                waypoint_store=self.store,
                plan_observer_dispatcher=dispatcher,
                initial_index=-1,
            )
        )
        self.selection = selection_provides.plan_selection_coordinator
        self.mutation: IPlanPointMutator = MutationFactory.create(
            MutationDependencies(
                waypoint_store=self.store,
                plan_history_saver=history_saver,
                plan_selection_navigator=selection_provides.plan_selection_navigator,
                plan_observer_dispatcher=dispatcher,
            )
        ).plan_point_mutator
        vp = ViewportTransform()
        self.state = CanvasInteractionState()
        mock_validator = MagicMock()
        mock_validator.validate_point.return_value.is_valid = True
        bundle = SelectionHandlerBundle(
            store=self.store,
            selection=self.selection,
            mutation=self.mutation,
            vp=vp,
            state=self.state,
            validator=mock_validator,
        )
        self.handler: CanvasSelectionMouseHandler = (
            CanvasSelectionMouseHandlerFactory.create(bundle)
        )

    def test_handle_select_down_hit(self) -> None:
        '''
            Tests waypoint selection on hit.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0, name='', command=''
        )
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
        pt = TrajectoryWaypoint(
            x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0, name='', command=''
        )
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
        pt = TrajectoryWaypoint(
            x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.handler.handle_select_down(10.0, 20.0)

        redraw: bool = self.handler.handle_select_drag(55.0, 65.0)
        self.assertFalse(redraw)
        updated: TrajectoryWaypoint = self.store.waypoints[0]
        self.assertEqual(updated.x, 55.0)
        self.assertEqual(updated.y, 65.0)

    def test_handle_select_drag_unselected(self) -> None:
        '''
            Tests unselected drag.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=10.0, y=20.0, z=15.0, phi=0.0, speed=30.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.state.dragged_node_idx = -1

        redraw: bool = self.handler.handle_select_drag(55.0, 65.0)
        self.assertFalse(redraw)
        unchanged: TrajectoryWaypoint = self.store.waypoints[0]
        self.assertEqual(unchanged.x, 10.0)
        self.assertEqual(unchanged.y, 20.0)

    def test_find_hit_index(self) -> None:
        '''
            Tests spatial hit detection query.

            :exceptions: None.
        '''
        pt1 = TrajectoryWaypoint(
            x=0.0, y=0.0, z=10.0, phi=0.0, speed=20.0, name='', command=''
        )
        pt2 = TrajectoryWaypoint(
            x=50.0, y=50.0, z=10.0, phi=0.0, speed=20.0, name='', command=''
        )
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
        pt = TrajectoryWaypoint(
            x=0.0, y=0.0, z=10.0, phi=0.0, speed=20.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.handler.handle_select_down(0.0, 0.0)
        self.assertEqual(self.selection.selected_index, 0)

        self.handler.clear_selection()
        self.assertEqual(self.selection.selected_index, -1)
        self.assertEqual(self.state.dragged_node_idx, -1)


if __name__ == '__main__':
    main()
