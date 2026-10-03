# -*- coding: UTF-8 -*-

'''
Module
    transport_factory.py
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
    Factory resolving and instantiating appropriate TransportBundle instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.driver.ichannel import IChannelDriver
from scarajectory.infrastructure.transport.driver.serial_channel_factory import SerialChannelDriverFactory
from scarajectory.infrastructure.transport.driver.tcp_channel_factory import TcpChannelDriverFactory
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.istream_transport_transceiver import IStreamTransportTransceiver
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener
from scarajectory.infrastructure.transport.listener.null_transport_listener import NullTransportListener
from scarajectory.infrastructure.transport.stream_transport_connection_factory import StreamTransportConnectionFactory
from scarajectory.infrastructure.transport.stream_transport_transceiver_factory import StreamTransportTransceiverFactory
from scarajectory.infrastructure.transport.listener.transport_listener_holder import TransportListenerHolder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransportFactory:
    '''
        Factory providing polymorphic transport resolution based on endpoint.

        It defines:

            :methods:
                | create_transport - Instantiates TransportBundle matching target endpoint.
                | create_default_transport - Instantiates default serial TransportBundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_transport(cls, endpoint: str) -> TransportBundle:
        '''
            Instantiates TransportBundle matching target endpoint identifier.

            :param endpoint: Port device path or host:port socket identifier.
            :return: TransportBundle instance.
            :exceptions: None.
        '''
        listener: ITransportListener = NullTransportListener()
        driver: IChannelDriver = (
            TcpChannelDriverFactory.create()
            if ':' in endpoint
            else SerialChannelDriverFactory.create()
        )
        holder: TransportListenerHolder = TransportListenerHolder(listener)
        connection: IStreamTransportConnection = (
            StreamTransportConnectionFactory.create(
                driver=driver,
                listener=holder,
            )
        )
        transceiver: IStreamTransportTransceiver = (
            StreamTransportTransceiverFactory.create(
                driver=driver,
                listener=holder,
                connection=connection,
            )
        )
        return TransportBundle(
            connection=connection,
            transceiver=transceiver,
        )

    @classmethod
    def create_default_transport(cls) -> TransportBundle:
        '''
            Instantiates default serial TransportBundle.

            :return: TransportBundle instance.
            :exceptions: None.
        '''
        return cls.create_transport('/dev/ttyUSB0')

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
