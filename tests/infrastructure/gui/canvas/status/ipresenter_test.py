# -*- coding: UTF-8 -*-

'''
Module
    ipresenter_test.py
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
    Unit tests for ICanvasStatusPresenter structural protocol interface.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.status.ipresenter import ICanvasStatusPresenter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestICanvasStatusPresenter(TestCase):
    '''
        Test cases verifying ICanvasStatusPresenter protocol definition.

        It defines:

            :methods:
                | test_mock_conformance - Verifies mock satisfies structural protocol.
                | test_non_conforming_object - Verifies object missing methods fails.
    '''

    def test_mock_conformance(self) -> None:
        '''
            Verifies structural mock satisfies ICanvasStatusPresenter.

            :exceptions: None.
        '''
        mock_presenter = MagicMock(spec=ICanvasStatusPresenter)
        self.assertIsInstance(mock_presenter, ICanvasStatusPresenter)

    def test_non_conforming_object(self) -> None:
        '''
            Verifies non-conforming object does not satisfy protocol.

            :exceptions: None.
        '''
        self.assertNotIsInstance(object(), ICanvasStatusPresenter)


if __name__ == '__main__':
    main()
