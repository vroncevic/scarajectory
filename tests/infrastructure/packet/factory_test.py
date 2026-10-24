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
    Unit testing for PacketFactory service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.packet.dependencies import PacketDependencies
from scarajectory.infrastructure.packet.factory import PacketFactory
from scarajectory.infrastructure.packet.provides import PacketProvides
from scarajectory.infrastructure.packet.strategy import BinaryPacketStrategy

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PacketFactoryTestCase(TestCase):
    '''Unit tests validating PacketFactory creation and versioning.'''

    def test_factory_creation(self) -> None:
        '''
            Verifies PacketFactory instantiates PacketProvides with BinaryPacketStrategy.

            :exceptions: None.
        '''
        deps = PacketDependencies(
            step_discretizer=MagicMock(),
            motion_frame_builder=MagicMock(),
            frame_packer=MagicMock(),
        )
        provides: PacketProvides = PacketFactory.create(deps)

        self.assertIsInstance(provides, PacketProvides)
        self.assertIsInstance(provides.packet_strategy, BinaryPacketStrategy)

    def test_factory_version(self) -> None:
        '''
            Verifies PacketFactory returns version string.

            :exceptions: None.
        '''
        self.assertEqual(PacketFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
