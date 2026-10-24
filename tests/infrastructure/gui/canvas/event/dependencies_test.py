# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for EventBinderDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.event.dependencies import EventBinderDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EventBinderDependenciesTestCase(TestCase):
    '''
        Unit tests for EventBinderDependencies dataclass.

        It defines:

            :methods:
                | test_init - Verifies bundle properties and immutability.
    '''

    def test_init(self) -> None:
        '''
            Verifies bundle properties and immutability.

            :exceptions: None.
        '''
        mock_canvas = MagicMock()
        mock_handler = MagicMock()
        mock_navigator = MagicMock()
        mock_presenter = MagicMock()
        deps = EventBinderDependencies(
            canvas=mock_canvas,
            mouse_handler=mock_handler,
            navigator=mock_navigator,
            status_presenter=mock_presenter,
        )
        self.assertIs(deps.canvas, mock_canvas)
        self.assertIs(deps.mouse_handler, mock_handler)
        self.assertIs(deps.navigator, mock_navigator)
        self.assertIs(deps.status_presenter, mock_presenter)


if __name__ == '__main__':
    main()
