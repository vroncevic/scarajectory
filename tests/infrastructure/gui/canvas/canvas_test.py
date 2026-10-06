# -*- coding: UTF-8 -*-

'''
Module
    canvas_test.py
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

from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_target import ICanvasViewTarget
from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.canvas.trajectory_canvas_factory import TrajectoryCanvasFactory
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


class TestTrajectoryCanvas(TestCase):
    '''
        Test cases verifying TrajectoryCanvas component behavior.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        mock_store = MagicMock()
        mock_selection = MagicMock()
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
        canvas_bundle = CanvasBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            dispatcher=self.mock_dispatcher,
            validator=mock_validator,
            settings=self.settings,
        )
        self.canvas: TrajectoryCanvas = TrajectoryCanvasFactory.create(
            self.root,
            bundle=canvas_bundle,
        )

    def tearDown(self) -> None:
        self.canvas.destroy()

    def test_satisfies_protocols(self) -> None:
        '''
            Verifies canvas satisfies ICanvas and ICanvasViewTarget.
        '''
        self.assertIsInstance(self.canvas, ICanvas)
        self.assertIsInstance(self.canvas, ICanvasViewTarget)

    def test_observer_registered_via_bridge(self) -> None:
        '''
            Verifies that observer bridge was registered with dispatcher.
        '''
        self.mock_dispatcher.add_observer.assert_called_once()

    def test_properties_exposure(self) -> None:
        '''
            Verifies tool_mode and settings property access.
        '''
        self.assertEqual(self.canvas.tool_mode, CanvasToolMode.POINT)
        self.assertEqual(self.canvas.settings, self.settings)

    def test_set_tool_mode_and_update_settings(self) -> None:
        '''
            Verifies tool mode setting and settings update.
        '''
        self.canvas.set_tool_mode(CanvasToolMode.LINE)
        self.assertEqual(self.canvas.tool_mode, CanvasToolMode.LINE)

        new_settings = CanvasSettings(
            default_z=30.0,
            default_speed=60.0,
            enforce_deadzone=False,
        )
        self.canvas.update_settings(new_settings)
        self.assertEqual(self.canvas.settings.default_z, 30.0)

    def test_get_view_dimensions(self) -> None:
        '''
            Verifies get_view_dimensions returns tuple of ints.
        '''
        w, h = self.canvas.get_view_dimensions()
        self.assertIsInstance(w, int)
        self.assertIsInstance(h, int)

    @patch.object(TrajectoryCanvas, 'winfo_width', return_value=800)
    @patch.object(TrajectoryCanvas, 'winfo_height', return_value=600)
    @patch('scarajectory.infrastructure.gui.canvas.trajectory_canvas.CanvasRenderer')
    def test_redraw_full_rendering(
        self,
        mock_renderer: MagicMock,
        mock_height: MagicMock,
        mock_width: MagicMock,
    ) -> None:
        '''
            Verifies redraw coordinates background, trajectory, and preview.
        '''
        self.canvas.redraw()
        mock_renderer.draw_background.assert_called_once()
        mock_renderer.draw_trajectory.assert_called_once()
        mock_renderer.draw_preview.assert_not_called()

        self.canvas._state.is_dragging = True
        self.canvas._state.drag_start_world = (10.0, 20.0)
        self.canvas._state.drag_current_world = (30.0, 40.0)
        self.canvas.redraw()
        self.assertEqual(mock_renderer.draw_preview.call_count, 1)


if __name__ == '__main__':
    main()
