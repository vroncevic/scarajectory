# -*- coding: UTF-8 -*-

'''
Module
    istrategy_test.py
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
    Unit tests for IPacketStrategy protocol.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.packet.strategy import BinaryPacketStrategy

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PacketStrategyProtocolTestCase(TestCase):
    '''Unit tests validating IPacketStrategy protocol conformance.'''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies BinaryPacketStrategy satisfies IPacketStrategy protocol.

            :exceptions: None.
        '''
        strategy = BinaryPacketStrategy(
            step_discretizer=MagicMock(),
            motion_frame_builder=MagicMock(),
            frame_packer=MagicMock(),
        )
        self.assertIsInstance(strategy, IPacketStrategy)


if __name__ == '__main__':
    main()
