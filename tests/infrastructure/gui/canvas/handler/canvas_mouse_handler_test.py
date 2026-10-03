# -*- coding: UTF-8 -*-

'''
Module
    canvas_mouse_handler_test.py
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
    Unit tests for CanvasMouseHandler CAD mouse interaction component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.mutation. \
    plan_mutation_service_factory import (
        PlanMutationServiceFactory,
    )
from scarajectory.core.service.trajectory.plan.observer. \
    plan_observer_dispatcher_factory import (
        PlanObserverDispatcherFactory,
    )
from scarajectory.core.service.trajectory.plan.selection. \
    plan_selection_coordinator_factory import (
        PlanSelectionCoordinatorFactory,
    )
from scarajectory.core.service.trajectory.plan.selection. \
    plan_selection_manager_factory import (
        PlanSelectionManagerFactory,
    )
from scarajectory.core.service.trajectory.plan.store. \
    waypoint_store_factory import (
        WaypointStoreFactory,
    )
from scarajectory.infrastructure.gui.canvas.handler.canvas_event_context import CanvasEventContext
from scarajectory.infrastructure.gui.canvas.handler.canvas_mouse_handler import CanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.canvas_mouse_handler_factory import CanvasMouseHandlerFactory
from scarajectory.infrastructure.gui.canvas.handler.mouse_handler_init_bundle import MouseHandlerInitBundle
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DummyEvent:
    '''
        Dummy event object mimicking Tkinter mouse event attributes.
    '''

    x: int
    y: int
    num: int
    delta: int

    def __init__(
        self,
        x: int,
        y: int,
        num: int = 1,
        delta: int = 0,
    ) -> None:
        self.x = x
        self.y = y
        self.num = num
        self.delta = delta

    def get_coords(self) -> tuple[int, int]:
        '''Returns event coordinates.'''
        return (self.x, self.y)

    def get_delta(self) -> int:
        '''Returns event scroll delta.'''
        return self.delta


class TestCanvasMouseHandler(TestCase):
    '''
        Test cases for CanvasMouseHandler mouse interaction logic.

        It defines:

            :methods:
                | setUp - Initializes fixtures for plan, viewport, handler.
                | test_mouse_down_panning - Tests pan with button 2 or 3.
                | test_mouse_down_select_hit - Tests waypoint selection.
                | test_mouse_drag_pan - Tests viewport pan movement.
                | test_mouse_up_point_tool - Tests committing point tool.
                | test_format_cursor_status - Tests formatting status readout.
    '''

    def setUp(self) -> None:
        '''
            Initializes fixtures for plan, viewport, and mouse handler.

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
        self.settings = CanvasSettings(default_z=15.0, default_speed=35.0)
        init_bundle = MouseHandlerInitBundle(
            store=self.store,
            selection=self.selection,
            mutation=self.mutation,
            vp=self.vp,
            state=self.state,
        )
        self.handler: CanvasMouseHandler = (
            CanvasMouseHandlerFactory.create_default(init_bundle)
        )

    def test_mouse_down_modes(self) -> None:
        '''Tests mouse down for panning, node selection, and freehand mode.'''
        pan_evt = DummyEvent(x=100, y=150, num=2)
        ctx_point = CanvasEventContext(
            800, 600, CanvasToolMode.POINT, self.settings
        )
        self.handler.handle_mouse_down(pan_evt, ctx_point)
        self.assertTrue(self.state.is_panning)

        self.state.is_panning = False
        pt = Waypoint(x=0.0, y=0.0, z=10.0, phi=0.0, speed=20.0)
        self.mutation.add_point(pt)
        select_evt = DummyEvent(x=400, y=300, num=1)
        ctx_select = CanvasEventContext(
            800, 600, CanvasToolMode.SELECT, self.settings
        )
        self.handler.handle_mouse_down(select_evt, ctx_select)
        self.assertEqual(self.state.dragged_node_idx, 0)
        self.assertEqual(self.selection.selected_index, 0)

        freehand_evt = DummyEvent(x=410, y=310, num=1)
        ctx_freehand = CanvasEventContext(
            800, 600, CanvasToolMode.FREEHAND, self.settings
        )
        self.handler.handle_mouse_down(freehand_evt, ctx_freehand)
        self.assertEqual(self.store.count, 2)

    def test_mouse_drag_modes(self) -> None:
        '''Tests mouse drag for pan, select, freehand, and shape tools.'''
        self.state.is_panning = True
        self.state.pan_x = 100
        self.state.pan_y = 100
        pan_evt = DummyEvent(x=120, y=115, num=1)
        ctx_point = CanvasEventContext(
            800, 600, CanvasToolMode.POINT, self.settings
        )
        self.assertTrue(self.handler.handle_mouse_drag(pan_evt, ctx_point))
        self.assertEqual(self.vp.pan_x, 20.0)

        self.state.is_panning = False
        ctx_select = CanvasEventContext(
            800, 600, CanvasToolMode.SELECT, self.settings
        )
        self.handler.handle_mouse_drag(pan_evt, ctx_select)

        ctx_freehand = CanvasEventContext(
            800, 600, CanvasToolMode.FREEHAND, self.settings
        )
        self.handler.handle_mouse_drag(pan_evt, ctx_freehand)

        ctx_circle = CanvasEventContext(
            800, 600, CanvasToolMode.CIRCLE, self.settings
        )
        self.assertTrue(self.handler.handle_mouse_drag(pan_evt, ctx_circle))

        self.assertFalse(self.handler.handle_mouse_drag(pan_evt, ctx_point))

    def test_mouse_up_and_stop_pan(self) -> None:
        '''Tests committing point on mouse up and releasing active pan.'''
        self.state.is_panning = True
        ctx_point = CanvasEventContext(
            800, 600, CanvasToolMode.POINT, self.settings
        )
        up_evt = DummyEvent(x=450, y=250, num=1)
        self.handler.handle_mouse_up(up_evt, ctx_point)
        self.assertFalse(self.state.is_panning)

        down_evt = DummyEvent(x=450, y=250, num=1)
        self.handler.handle_mouse_down(down_evt, ctx_point)
        self.handler.handle_mouse_up(up_evt, ctx_point)
        self.assertGreaterEqual(self.store.count, 1)
        self.assertIsNone(self.state.drag_start_world)

    def test_format_cursor_status_and_factory(self) -> None:
        '''Tests status bar readout text and factory version.'''
        event = DummyEvent(x=400, y=300)
        status_text = self.handler.format_cursor_status(event, 800, 600)
        self.assertIn('Cursor: X=', status_text)
        self.assertIn('Zoom:', status_text)
        self.assertEqual(CanvasMouseHandlerFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
