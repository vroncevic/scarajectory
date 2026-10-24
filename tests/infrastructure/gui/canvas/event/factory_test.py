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
    Unit tests for CanvasEventBinderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.event.binder import CanvasEventBinder
from scarajectory.infrastructure.gui.canvas.event.dependencies import EventBinderDependencies
from scarajectory.infrastructure.gui.canvas.event.factory import CanvasEventBinderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasEventBinderFactoryTestCase(TestCase):
    '''
        Unit tests for CanvasEventBinderFactory.

        It defines:

            :methods:
                | test_create - Verifies CanvasEventBinder instantiation.
                | test_get_version - Verifies factory version retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies CanvasEventBinder instantiation.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        mock_handler = MagicMock()
        mock_navigator = MagicMock()
        mock_presenter = MagicMock()
        binder: CanvasEventBinder = CanvasEventBinderFactory.create(
            EventBinderDependencies(
                canvas=mock_canvas,
                mouse_handler=mock_handler,
                navigator=mock_navigator,
                status_presenter=mock_presenter,
            )
        )
        self.assertIsInstance(binder, CanvasEventBinder)

    def test_get_version(self) -> None:
        '''
            Verifies factory version retrieval.

            :exceptions: None.
        '''
        self.assertEqual(CanvasEventBinderFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
