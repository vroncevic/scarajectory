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
    Unit tests for CanvasPreviewRenderer.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.renderer.preview.renderer import CanvasPreviewRenderer
from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasPreviewRendererTestCase(TestCase):
    '''
        Test cases for CanvasPreviewRenderer.

        It defines:

            :methods:
                | test_draw_preview_line - Tests drawing line preview.
                | test_draw_preview_rectangle - Tests drawing rectangle preview.
                | test_draw_preview_circle - Tests drawing circle preview.
                | test_get_version - Tests component version string query.
    '''

    def test_draw_preview_line(self) -> None:
        '''
            Tests drawing line preview.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        mock_canvas.winfo_width.return_value = 800
        mock_canvas.winfo_height.return_value = 600
        vp = ViewportTransform()
        drag_points = ((0.0, 0.0), (100.0, 100.0))

        CanvasPreviewRenderer.draw_preview(
            mock_canvas, vp, CanvasToolMode.LINE, drag_points
        )
        mock_canvas.create_line.assert_called_once()

    def test_draw_preview_rectangle(self) -> None:
        '''
            Tests drawing rectangle preview.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        mock_canvas.winfo_width.return_value = 800
        mock_canvas.winfo_height.return_value = 600
        vp = ViewportTransform()
        drag_points = ((0.0, 0.0), (100.0, 100.0))

        CanvasPreviewRenderer.draw_preview(
            mock_canvas, vp, CanvasToolMode.RECTANGLE, drag_points
        )
        mock_canvas.create_rectangle.assert_called_once()

    def test_draw_preview_circle(self) -> None:
        '''
            Tests drawing circle preview.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        mock_canvas.winfo_width.return_value = 800
        mock_canvas.winfo_height.return_value = 600
        vp = ViewportTransform()
        drag_points = ((0.0, 0.0), (100.0, 100.0))

        CanvasPreviewRenderer.draw_preview(
            mock_canvas, vp, CanvasToolMode.CIRCLE, drag_points
        )
        mock_canvas.create_oval.assert_called_once()
        mock_canvas.create_line.assert_called_once()

    def test_get_version(self) -> None:
        '''
            Tests component version string query.

            :exceptions: None.
        '''
        self.assertEqual(CanvasPreviewRenderer.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
