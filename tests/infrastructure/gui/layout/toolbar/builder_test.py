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
    Unit testing for ToolbarLayoutBuilder component.
'''

from __future__ import annotations

from tkinter import TOP, X
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
from scarajectory.infrastructure.gui.dependencies import GUIDependencies
from scarajectory.infrastructure.gui.layout.toolbar.builder import ToolbarLayoutBuilder
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarLayoutBuilderTestCase(TestCase):
    '''
        Unit tests for ToolbarLayoutBuilder.

        It defines:

            :methods:
                | test_build_toolbar - Verifies top toolbar construction and mounting.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_build_toolbar(self) -> None:
        '''
            Verifies build constructs and mounts toolbar widget.

            :exceptions: None.
        '''
        mock_root = MagicMock()
        mock_canvas = MagicMock(spec=TrajectoryCanvas)
        mock_canvas.navigator = MagicMock()
        mock_canvas.status_presenter = MagicMock()
        mock_toolbar = MagicMock(spec=Toolbar)
        mock_factory = MagicMock()
        mock_factory.create.return_value = mock_toolbar

        mock_bundle = MagicMock(spec=GUIDependencies)
        mock_settings = MagicMock(spec=CanvasSettings)

        builder = ToolbarLayoutBuilder(toolbar_factory=mock_factory)
        toolbar = builder.build(
            mock_root,
            canvas=mock_canvas,
            bundle=mock_bundle,
            settings=mock_settings,
        )

        mock_factory.create.assert_called_once()
        mock_toolbar.pack.assert_called_once_with(side=TOP, fill=X)
        self.assertIs(toolbar, mock_toolbar)

    def test_get_version(self) -> None:
        '''
            Verifies get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = ToolbarLayoutBuilder(toolbar_factory=MagicMock()).get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
