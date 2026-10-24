# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for CanvasMouseHandlerFactory service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.mouse.bundle import MouseHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.mouse.factory import CanvasMouseHandlerFactory
from scarajectory.infrastructure.gui.canvas.handler.mouse.handler import CanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.mouse.init_bundle import MouseHandlerInitBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasMouseHandlerFactoryTestCase(TestCase):
    '''
        Unit tests for CanvasMouseHandlerFactory.

        It defines:

            :methods:
                | test_create - Verifies explicit bundle construction.
                | test_create_default - Verifies default construction wiring.
                | test_get_version - Verifies factory version return.
    '''

    def test_create(self) -> None:
        '''
            Verifies CanvasMouseHandlerFactory creates instance from bundle.

            :exceptions: None.
        '''
        mock_bundle = MagicMock(spec=MouseHandlerBundle)
        handler = CanvasMouseHandlerFactory.create(mock_bundle)
        self.assertIsInstance(handler, CanvasMouseHandler)

    def test_create_default(self) -> None:
        '''
            Verifies CanvasMouseHandlerFactory creates instance from init bundle.

            :exceptions: None.
        '''
        mock_init_bundle = MagicMock(spec=MouseHandlerInitBundle)
        mock_init_bundle.store = MagicMock()
        mock_init_bundle.selection = MagicMock()
        mock_init_bundle.mutation = MagicMock()
        mock_init_bundle.bulk_mutator = MagicMock()
        mock_init_bundle.vp = MagicMock()
        mock_init_bundle.state = MagicMock()
        mock_init_bundle.avoidance_adapter = MagicMock()
        mock_init_bundle.planner_adapter = MagicMock()

        handler = CanvasMouseHandlerFactory.create_default(mock_init_bundle)
        self.assertIsInstance(handler, CanvasMouseHandler)

    def test_get_version(self) -> None:
        '''
            Verifies CanvasMouseHandlerFactory returns correct version string.

            :exceptions: None.
        '''
        version = CanvasMouseHandlerFactory.get_version()
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
