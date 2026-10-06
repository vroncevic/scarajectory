# -*- coding: UTF-8 -*-

'''
Module
    stream_raw_transceiver_factory.py
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
    Factory service constructing StreamRawTransceiver adapter instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.connection.stream_raw_transceiver import StreamRawTransceiver
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection
from scarajectory.infrastructure.transport.istream_transport_transceiver import IStreamTransportTransceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamRawTransceiverFactory:
    '''
    Factory providing creation of StreamRawTransceiver instances.

    It defines:

        :methods:
            | create - Constructs StreamRawTransceiver with connection and transceiver.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        connection: IStreamTransportConnection,
        transceiver: IStreamTransportTransceiver,
    ) -> StreamRawTransceiver:
        '''
        Constructs and returns a StreamRawTransceiver instance.

        :param connection: Injected IStreamTransportConnection instance.
        :param transceiver: Injected IStreamTransportTransceiver instance.
        :return: Configured StreamRawTransceiver instance.
        :exceptions: None.
        '''
        return StreamRawTransceiver(
            connection=connection,
            transceiver=transceiver,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Factory version string.
        :exceptions: None.
        '''
        return __version__
