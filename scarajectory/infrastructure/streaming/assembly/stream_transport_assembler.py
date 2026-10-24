# -*- coding: UTF-8 -*-

'''
Module
    stream_transport_assembler.py
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
    Assembles physical connection manager, transceiver, and coordinator for streaming.
'''

from __future__ import annotations

from typing import cast

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator
from scaracom.bridge.dependencies import BridgeDependencies
from scaracom.bridge.factory import BridgeFactory
from scaracom.bridge.listener.itransport_listener import ITransportListener
from scaracom.bridge.provides import BridgeProvides
from scaracom.bridge.transceiver.transceiver import RawTransceiver
from scaracom.transport.itransport import ITransport

from scarajectory.infrastructure.connection.manager.dependencies import ManagerDependencies
from scarajectory.infrastructure.connection.manager.factory import ManagerFactory
from scarajectory.infrastructure.connection.manager.manager import ConnectionManager
from scarajectory.infrastructure.connection.manager.provides import ManagerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportAssembler:
    '''
        Sub-assembler for connection manager, raw transceiver, and coordinator components.

        It defines:

            :methods:
                | assemble - Constructs connection manager, transceiver, and coordinator.
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(
        cls,
        transport: ITransport,
        *,
        listener: ITransportListener,
    ) -> tuple[ConnectionManager, RawTransceiver, IConnectionCoordinator]:
        '''
            Constructs and returns connection manager, transceiver, and coordinator tuple.

            :param transport: Injected ITransport communication layer instance.
            :param listener: Injected ITransportListener event sink instance.
            :return: Tuple of (ConnectionManager, RawTransceiver, IConnectionCoordinator).
            :exceptions: None.
        '''
        bridge_provides: BridgeProvides = BridgeFactory.create(
            BridgeDependencies(
                transport=transport,
                listener=listener,
            )
        )
        conn_provides: ManagerProvides = ManagerFactory.create(
            ManagerDependencies(
                connection_coordinator=bridge_provides.coordinator,
            )
        )

        return (
            conn_provides.connection_manager,
            cast(RawTransceiver, bridge_provides.transceiver),
            bridge_provides.coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
