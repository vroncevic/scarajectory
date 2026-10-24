# -*- coding: UTF-8 -*-

'''
Module
    trajectory_canvas_test.py
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
    Unit tests for TrajectoryCanvas component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.core.service.trajectory.plan.mutation.provides import MutationProvides
from scarajectory.infrastructure.gui.canvas.adapter_bundle import CanvasAdapterBundle
from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.canvas.navigation.itarget import ICanvasViewTarget
from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.canvas.trajectory_canvas_factory import TrajectoryCanvasFactory
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryCanvasTestCase(TestCase):
    '''
        Test cases verifying TrajectoryCanvas component behavior.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | setUp - Sets up canvas component and mocks.
                | tearDown - Tears down canvas widget.
                | test_satisfies_protocols - Verifies canvas satisfies structural protocols.
                | test_observer_and_properties - Verifies observer and property interactions.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tk fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down root Tk fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up canvas component and mocks.

            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_store.waypoints = ()
        mock_selection = MagicMock()
        mock_selection.selected_index = -1
        mock_mutation = MagicMock()
        self.mock_dispatcher = MagicMock()
        mock_validator = MagicMock()
        mock_validator.r_max = 350.0
        mock_validator.r_min = 50.0
        self.settings = CanvasSettings(
            default_z=20.0,
            default_speed=50.0,
            enforce_deadzone=True,
        )
        mock_avoidance = MagicMock()
        mock_avoidance.crosses_dead_zone.return_value = False
        mock_avoidance.plan_detour.return_value = []
        canvas_bundle = CanvasBundle(
            store=mock_store,
            selection=mock_selection,
            mutations=MutationProvides(
                plan_point_mutator=mock_mutation,
                plan_bulk_mutator=MagicMock(),
            ),
            dispatcher=self.mock_dispatcher,
            validator=mock_validator,
            settings=self.settings,
            adapters=CanvasAdapterBundle(
                avoidance=mock_avoidance,
                planner=MagicMock(),
                boundary=MagicMock(),
            ),
        )
        self.canvas_bundle = canvas_bundle
        self.canvas: TrajectoryCanvas = TrajectoryCanvasFactory.create(
            self.root,
            bundle=canvas_bundle,
        )

    def tearDown(self) -> None:
        '''
            Tears down canvas widget.

            :exceptions: None.
        '''
        self.canvas.destroy()

    def test_satisfies_protocols(self) -> None:
        '''
            Verifies canvas satisfies ICanvas and ICanvasViewTarget.

            :exceptions: None.
        '''
        self.assertIsInstance(self.canvas, ICanvas)
        self.assertIsInstance(self.canvas, ICanvasViewTarget)

    def test_observer_and_properties(self) -> None:
        '''
            Verifies observer registration, properties, and update_settings.

            :exceptions: None.
        '''
        self.mock_dispatcher.add_observer.assert_called_once()
        self.assertEqual(self.canvas.tool_mode, CanvasToolMode.POINT)
        self.assertEqual(self.canvas.settings, self.settings)

        self.canvas.set_tool_mode(CanvasToolMode.LINE)
        self.assertEqual(self.canvas.tool_mode, CanvasToolMode.LINE)

        new_settings = CanvasSettings(
            default_z=30.0,
            default_speed=60.0,
            enforce_deadzone=False,
        )
        self.canvas.update_settings(new_settings)
        self.assertEqual(self.canvas.settings.default_z, 30.0)

        w, h = self.canvas.get_view_dimensions()
        self.assertIsInstance(w, int)
        self.assertIsInstance(h, int)

        dragging_state = CanvasInteractionState()
        dragging_state.is_dragging = True
        preview_canvas = TrajectoryCanvas(
            self.root,
            bundle=self.canvas_bundle,
            vp=ViewportTransform(),
            state=dragging_state,
        )
        with patch.object(preview_canvas, 'winfo_width', return_value=800), \
             patch.object(preview_canvas, 'winfo_height', return_value=600):
            preview_canvas.redraw()
        preview_canvas.destroy()


if __name__ == '__main__':
    main()
