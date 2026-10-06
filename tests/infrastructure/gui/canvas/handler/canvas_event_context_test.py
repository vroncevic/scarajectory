# -*- coding: UTF-8 -*-

'''
Module
    canvas_event_context_test.py
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
    Unit testing for CanvasEventContext data model.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.canvas_event_context import CanvasEventContext
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasEventContextTestCase(TestCase):
    '''
        Unit tests for CanvasEventContext.

        It defines:

            :methods:
                | test_context_creation_and_attributes - Verifies context fields.
    '''

    def test_context_creation_and_attributes(self) -> None:
        '''Verifies CanvasEventContext stores and exposes viewport geometry.'''
        mock_settings = MagicMock()
        context = CanvasEventContext(
            width=800,
            height=600,
            tool_mode=CanvasToolMode.SELECT,
            settings=mock_settings,
        )

        self.assertEqual(context.width, 800)
        self.assertEqual(context.height, 600)
        self.assertEqual(context.tool_mode, CanvasToolMode.SELECT)
        self.assertIs(context.settings, mock_settings)


if __name__ == '__main__':
    main()
