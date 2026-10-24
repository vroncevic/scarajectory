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
    Unit testing for StreamingDependencies dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.transport.itransport import ITransport

from scarajectory.infrastructure.streaming.dependencies import StreamingDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamingDependencies(TestCase):
    '''
    Test cases verifying StreamingDependencies parameter bundle.

    It defines:

        :methods:
            | test_initialization - Tests attributes and defaults.
            | test_frozen - Tests immutability constraint.
    '''

    def test_initialization(self) -> None:
        '''
        Tests initialization of StreamingDependencies.

        :exceptions: None.
        '''
        transport = MagicMock(spec=ITransport)
        deps = StreamingDependencies(transport=transport)
        self.assertIs(deps.transport, transport)
        self.assertEqual(deps.queue_capacity, 16)

    def test_frozen(self) -> None:
        '''
        Tests immutability of StreamingDependencies.

        :exceptions: None.
        '''
        transport = MagicMock(spec=ITransport)
        deps = StreamingDependencies(transport=transport)
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'queue_capacity', 32)


if __name__ == '__main__':
    main()
