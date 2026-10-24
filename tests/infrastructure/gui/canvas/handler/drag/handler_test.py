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
    Unit tests for CanvasDragHandler dragging motion component.
'''

from __future__ import annotations

from typing import ClassVar
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
from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.infrastructure.gui.canvas.handler.drag.bundle import DragHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.drag.handler import CanvasDragHandler
from scarajectory.infrastructure.gui.canvas.handler.drag.factory import CanvasDragHandlerFactory
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
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
                | test_drag_freehand_ignores_below_threshold - Tests ignoring freehand point below threshold.
                | test_drag_select_ignores_when_target_in_dead_zone - Tests drag select ignores dead zone targets.
                | test_drag_freehand_ignores_when_point_in_dead_zone - Tests freehand drag ignores dead zone points.
                | test_drag_freehand_detours_when_crossing_dead_zone - Tests detour insertion on dead zone crossing.
    '''

    SETTINGS: ClassVar[CanvasSettings] = CanvasSettings(default_z=10.0, default_speed=25.0)

    store: IWaypointStore
    mutation: IPlanPointMutator
    state: CanvasInteractionState
    avoidance: MagicMock
    shape_mock: MagicMock
    validator: MagicMock
    drag_handler: CanvasDragHandler

    def setUp(self) -> None:
        '''
            Initializes fixtures for store, mutation, shape handler, and drag handler.

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
        self.mutation: IPlanPointMutator = MutationFactory.create(
            MutationDependencies(
                waypoint_store=self.store,
                plan_history_saver=history_saver,
                plan_selection_navigator=selection_provides.plan_selection_navigator,
                plan_observer_dispatcher=dispatcher,
            )
        ).plan_point_mutator
        self.state = CanvasInteractionState()
        self.avoidance = MagicMock()
        self.avoidance.is_point_in_dead_zone.return_value = False
        self.avoidance.crosses_dead_zone.return_value = False

        self.shape_mock = MagicMock()
        self.shape_mock.create_relocated_waypoint.side_effect = (
            lambda cur, wx, wy: TrajectoryWaypoint(
                x=wx,
                y=wy,
                z=cur.z,
                phi=cur.phi,
                speed=cur.speed,
                name=cur.name,
                command=cur.command,
            )
        )
        self.shape_mock.create_waypoint_at.side_effect = (
            lambda wx, wy, s: TrajectoryWaypoint(
                x=wx,
                y=wy,
                z=s.default_z,
                phi=0.0,
                speed=s.default_speed,
                name='',
                command='',
            )
        )

        mock_validator = MagicMock()
        mock_validator.validate_point.return_value.is_valid = True
        self.validator = mock_validator

        drag_bundle = DragHandlerBundle(
            store=self.store,
            mutation=self.mutation,
            state=self.state,
            shape_handler=self.shape_mock,
            avoidance_adapter=self.avoidance,
            validator=mock_validator,
        )
        self.drag_handler = CanvasDragHandlerFactory.create(drag_bundle)

    def test_drag_select_updates_point(self) -> None:
        '''
            Tests updating waypoint location during select drag.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=10.0, y=10.0, z=5.0, phi=0.0, speed=15.0, name='', command=''
        )
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

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=10.0, y=10.0, z=5.0, phi=0.0, speed=15.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.state.dragged_node_idx = -1

        redraw = self.drag_handler.handle_drag_select(wx=50.0, wy=60.0)
        self.assertFalse(redraw)
        self.assertEqual(self.store.waypoints[0].x, 10.0)

    def test_drag_freehand_appends_when_threshold_met(self) -> None:
        '''
            Tests appending point during freehand drag when distance threshold is met.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=0.0, y=0.0, z=10.0, phi=0.0, speed=25.0, name='', command=''
        )
        self.mutation.add_point(pt)

        redraw = self.drag_handler.handle_drag_freehand(
            wx=10.0, wy=0.0, settings=self.SETTINGS
        )
        self.assertFalse(redraw)
        self.assertEqual(self.store.count, 2)
        self.assertEqual(self.store.waypoints[1].x, 10.0)

    def test_drag_freehand_ignores_below_threshold(self) -> None:
        '''
            Tests ignoring freehand point below distance threshold.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=0.0, y=0.0, z=10.0, phi=0.0, speed=25.0, name='', command=''
        )
        self.mutation.add_point(pt)

        redraw = self.drag_handler.handle_drag_freehand(
            wx=1.0, wy=0.0, settings=self.SETTINGS
        )
        self.assertFalse(redraw)
        self.assertEqual(self.store.count, 1)

    def test_drag_select_ignores_when_target_in_dead_zone(self) -> None:
        '''
            Tests drag select does not update waypoint when target is in dead zone.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=10.0, y=10.0, z=5.0, phi=0.0, speed=15.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.state.dragged_node_idx = 0
        self.avoidance.is_point_in_dead_zone.return_value = True

        redraw = self.drag_handler.handle_drag_select(wx=5.0, wy=5.0)
        self.assertFalse(redraw)
        self.assertEqual(self.store.waypoints[0].x, 10.0)

    def test_drag_freehand_ignores_when_point_in_dead_zone(self) -> None:
        '''
            Tests freehand drag ignores points in dead zone.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=50.0, y=50.0, z=10.0, phi=0.0, speed=25.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.avoidance.is_point_in_dead_zone.return_value = True

        redraw = self.drag_handler.handle_drag_freehand(
            wx=10.0, wy=10.0, settings=self.SETTINGS
        )
        self.assertFalse(redraw)
        self.assertEqual(self.store.count, 1)

        self.avoidance.is_point_in_dead_zone.return_value = False
        self.validator.validate_point.return_value.is_valid = False
        redraw = self.drag_handler.handle_drag_freehand(
            wx=20.0, wy=20.0, settings=self.SETTINGS
        )
        self.assertFalse(redraw)
        self.validator.validate_point.return_value.is_valid = True

    def test_drag_freehand_detours_when_crossing_dead_zone(self) -> None:
        '''
            Tests freehand drag inserts bypass waypoints when segment crosses dead zone.

            :exceptions: None.
        '''
        pt = TrajectoryWaypoint(
            x=120.0, y=-50.0, z=10.0, phi=0.0, speed=25.0, name='', command=''
        )
        self.mutation.add_point(pt)
        self.avoidance.crosses_dead_zone.return_value = True
        detour = [
            TrajectoryWaypoint(
                x=95.0, y=10.0, z=10.0, speed=25.0, phi=0.0, name='', command=''
            ),
            TrajectoryWaypoint(
                x=-120.0, y=50.0, z=10.0, speed=25.0, phi=0.0, name='', command=''
            ),
        ]
        self.avoidance.plan_detour.return_value = detour

        def validate_detour(wp: TrajectoryWaypoint) -> MagicMock:
            res: MagicMock = MagicMock()
            res.is_valid = wp.x != 95.0
            return res

        self.validator.validate_point.side_effect = validate_detour
        redraw = self.drag_handler.handle_drag_freehand(
            wx=-120.0, wy=50.0, settings=self.SETTINGS
        )
        self.assertFalse(redraw)
        self.validator.validate_point.side_effect = None
        self.validator.validate_point.return_value.is_valid = True


        redraw = self.drag_handler.handle_drag_freehand(
            wx=-120.0, wy=50.0, settings=self.SETTINGS
        )
        self.assertFalse(redraw)
        self.assertEqual(self.store.count, 3)
        self.assertEqual(self.store.waypoints[1].x, 95.0)
        self.assertEqual(self.store.waypoints[2].x, -120.0)


if __name__ == '__main__':
    main()
