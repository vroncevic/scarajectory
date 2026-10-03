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
    Assembles physical connection manager and transceiver for streaming.
'''

from __future__ import annotations

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.connection.stream_connection_manager_factory import StreamConnectionManagerFactory
from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.connection.stream_raw_transceiver_factory import StreamRawTransceiverFactory
from scarajectory.infrastructure.transport.bundle import TransportBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportAssembler:
    '''
        Sub-assembler for connection manager and raw transceiver components.

        It defines:

            :methods:
                | assemble - Constructs connection manager and transceiver.
                | get_version - Returns assembler version string.
    '''

    @classmethod
    def assemble(
        cls,
        transport: TransportBundle,
        *,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> tuple[StreamConnectionManager, StreamRawTransceiver]:
        '''
            Constructs and returns connection manager and transceiver tuple.

            :param transport: TransportBundle parameter instance.
            :param protocol_mode: Active protocol mode.
            :return: Tuple of (StreamConnectionManager, StreamRawTransceiver).
            :exceptions: None.
        '''
        conn_manager: StreamConnectionManager = (
            StreamConnectionManagerFactory.create(
                connection=transport.connection,
                protocol_mode=protocol_mode,
            )
        )
        raw_transceiver: StreamRawTransceiver = (
            StreamRawTransceiverFactory.create(
                connection=transport.connection,
                transceiver=transport.transceiver,
            )
        )

        return conn_manager, raw_transceiver

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns assembler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
