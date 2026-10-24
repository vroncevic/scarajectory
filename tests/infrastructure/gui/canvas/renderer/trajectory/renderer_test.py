# -*- coding: UTF-8 -*-

'''
Module
    renderer_test.py
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
    Unit tests for CanvasTrajectoryRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.bundle import TrajectoryRenderBundle
from scarajectory.infrastructure.gui.canvas.renderer.trajectory.renderer import CanvasTrajectoryRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasTrajectoryRendererTestCase(TestCase):
    '''
        Test cases for CanvasTrajectoryRenderer.

        It defines:

            :methods:
                | test_draw_trajectory_empty - Tests drawing when waypoint store is empty.
                | test_draw_trajectory_with_points - Tests drawing trajectory path and selections.
                | test_get_version - Tests get_version returns string.
    '''

    def test_draw_trajectory_empty(self) -> None:
        '''
            Tests drawing when waypoint store is empty.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        vp = ViewportTransform()
        mock_store = MagicMock()
        mock_store.waypoints = ()
        mock_selection = MagicMock()
        mock_selection.selected_index = -1
        mock_validator = MagicMock()
        bundle = TrajectoryRenderBundle(
            store=mock_store, selection=mock_selection, validator=mock_validator
        )

        CanvasTrajectoryRenderer.draw_trajectory(mock_canvas, vp, bundle)
        mock_canvas.create_line.assert_not_called()

    def test_draw_trajectory_with_points(self) -> None:
        '''
            Tests drawing trajectory path and selections.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        mock_canvas.winfo_width.return_value = 800
        mock_canvas.winfo_height.return_value = 600
        vp = ViewportTransform()
        mock_store = MagicMock()
        mock_store.waypoints = [
            TrajectoryWaypoint(x=100.0, y=100.0, z=0.0, phi=0.0, speed=100.0, name='', command=''),
            TrajectoryWaypoint(x=150.0, y=150.0, z=0.0, phi=0.0, speed=100.0, name='', command=''),
        ]
        mock_selection = MagicMock()
        mock_selection.selected_index = 0
        mock_validator = MagicMock()
        mock_validator.validate_point.return_value.is_valid = True
        bundle = TrajectoryRenderBundle(
            store=mock_store, selection=mock_selection, validator=mock_validator
        )

        CanvasTrajectoryRenderer.draw_trajectory(mock_canvas, vp, bundle)
        self.assertGreater(mock_canvas.create_line.call_count, 0)
        self.assertGreater(mock_canvas.create_oval.call_count, 0)

    def test_get_version(self) -> None:
        '''
            Tests get_version returns component version string.

            :exceptions: None.
        '''
        version: str = CanvasTrajectoryRenderer.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
