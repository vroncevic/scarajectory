# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit testing for ConnectionProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator
from scaracom.bridge.transceiver.ichannel import IRawChannel
from scaracom.flow.router.irouter import IFrameRouter

from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.connection.provides import ConnectionProvides


class ConnectionProvidesTestCase(TestCase):
    '''
        Test cases for ConnectionProvides container.

        It defines:

            :methods:
                | test_container_attributes - Verifies container stores and exposes connection role interfaces.
    '''

    def test_container_attributes(self) -> None:
        '''
            Verifies container stores and exposes connection role interfaces.

            :exceptions: None.
        '''
        mock_mgr = MagicMock(spec=IConnectionManager)
        mock_xceiver = MagicMock(spec=IRawChannel)
        mock_disp = MagicMock(spec=IChannelDispatcher)
        mock_router = MagicMock(spec=IFrameRouter)
        mock_coord = MagicMock(spec=IConnectionCoordinator)

        provides = ConnectionProvides(
            connection_manager=mock_mgr,
            raw_channel=mock_xceiver,
            channel_dispatcher=mock_disp,
            frame_router=mock_router,
            connection_coordinator=mock_coord,
        )
        self.assertIs(provides.connection_manager, mock_mgr)
        self.assertIs(provides.raw_channel, mock_xceiver)
        self.assertIs(provides.channel_dispatcher, mock_disp)
        self.assertIs(provides.frame_router, mock_router)
        self.assertIs(provides.connection_coordinator, mock_coord)


if __name__ == '__main__':
    main()
