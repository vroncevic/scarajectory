# -*- coding: UTF-8 -*-

'''
Module
    builder_test.py
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
    Unit testing for CanvasPaneBuilder component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.layout.canvas.builder import CanvasPaneBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasPaneBuilderTestCase(TestCase):
    '''
        Unit tests for CanvasPaneBuilder.

        It defines:

            :methods:
                | test_build_canvas_pane - Verifies canvas pane construction and mounting.
                | test_get_version - Verifies version string retrieval.
    '''

    @patch('scarajectory.infrastructure.gui.layout.canvas.builder.Frame')
    def test_build_canvas_pane(self, mock_frame_cls: MagicMock) -> None:
        '''
            Verifies build mounts frame on parent and instantiates canvas.

            :param mock_frame_cls: Mocked ttk.Frame constructor.
            :exceptions: None.
        '''
        mock_parent = MagicMock()
        mock_frame = MagicMock()
        mock_frame_cls.return_value = mock_frame

        mock_canvas = MagicMock(spec=TrajectoryCanvas)
        mock_factory = MagicMock()
        mock_factory.create.return_value = mock_canvas

        mock_bundle = MagicMock(spec=GUIDependencies)
        mock_settings = MagicMock(spec=CanvasSettings)

        builder = CanvasPaneBuilder(canvas_factory=mock_factory)
        canvas = builder.build(
            mock_parent,
            bundle=mock_bundle,
            settings=mock_settings,
        )

        mock_parent.add.assert_called_once_with(
            mock_frame, weight=CanvasPaneBuilder.WEIGHT
        )
        mock_factory.create.assert_called_once()
        mock_canvas.pack.assert_called_once()
        self.assertIs(canvas, mock_canvas)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = CanvasPaneBuilder(canvas_factory=MagicMock()).get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
