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
    Unit testing for ConnectionFactory coordinator.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator
from scaracom.bridge.transceiver.ichannel import IRawChannel
from scaracom.flow.router.irouter import IFrameRouter

from scarajectory.infrastructure.connection.dependencies import ConnectionDependencies
from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.connection.factory import ConnectionFactory
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.connection.provides import ConnectionProvides


class ConnectionFactoryTestCase(TestCase):
    '''
        Test cases for ConnectionFactory root coordinator.
    '''

    def test_create(self) -> None:
        '''
            Verifies root factory wires all subsystems and returns ConnectionProvides.

            :exceptions: None.
        '''
        deps = ConnectionDependencies(
            transport=MagicMock(),
            frame_packer=MagicMock(),
            listener=MagicMock(),
        )
        provides = ConnectionFactory.create(deps)
        self.assertIsInstance(provides, ConnectionProvides)
        self.assertIsInstance(provides.connection_manager, IConnectionManager)
        self.assertIsInstance(provides.raw_channel, IRawChannel)
        self.assertIsInstance(provides.channel_dispatcher, IChannelDispatcher)
        self.assertIsInstance(provides.frame_router, IFrameRouter)
        self.assertIsInstance(provides.connection_coordinator, IConnectionCoordinator)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns version string.

            :exceptions: None.
        '''
        self.assertIsInstance(ConnectionFactory.get_version(), str)


if __name__ == '__main__':
    main()
