# -*- coding: UTF-8 -*-

'''
Module
    toolbar_layout_builder_test.py
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
    Unit tests for ToolbarLayoutBuilder and ToolbarLayoutBuilderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.layout.itoolbar_layout_builder import IToolbarLayoutBuilder
from scarajectory.infrastructure.gui.layout.toolbar_layout_builder import ToolbarLayoutBuilder
from scarajectory.infrastructure.gui.layout.toolbar_layout_builder_factory import ToolbarLayoutBuilderFactory
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolbarLayoutBuilder(TestCase):
    '''
        Unit test cases verifying ToolbarLayoutBuilder component and factory.
    '''

    mock_bundle: MagicMock

    def setUp(self) -> None:
        validator = MagicMock()
        validator.r_min = 25.0
        validator.r_max = 280.0
        self.mock_bundle = MagicMock()
        self.mock_bundle.validator = validator

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs instance implementing IToolbarLayoutBuilder.
        '''
        builder = ToolbarLayoutBuilderFactory.create()
        self.assertIsInstance(builder, IToolbarLayoutBuilder)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(ToolbarLayoutBuilderFactory.get_version(), str)

    def test_build(self) -> None:
        '''
            Verifies build creates and packs toolbar in the root window.
        '''
        mock_toolbar = MagicMock()
        mock_factory = MagicMock()
        mock_factory.create.return_value = mock_toolbar

        builder = ToolbarLayoutBuilder(toolbar_factory=mock_factory)
        root = MagicMock()
        settings = CanvasSettings(
            default_z=20.0,
            default_speed=50.0,
            enforce_deadzone=True,
        )
        result = builder.build(
            root,
            canvas=MagicMock(),
            bundle=self.mock_bundle,
            settings=settings,
        )
        self.assertEqual(result, mock_toolbar)
        mock_toolbar.pack.assert_called_once()
        self.assertIsInstance(builder.get_version(), str)


if __name__ == '__main__':
    main()
