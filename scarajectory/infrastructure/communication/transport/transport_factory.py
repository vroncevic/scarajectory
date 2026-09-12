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
    Factory resolving and instantiating appropriate ITransport implementations.
'''

from __future__ import annotations

from scarajectory.infrastructure.communication.transport.itransport import ITransport
from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
from scarajectory.infrastructure.communication.transport.tcp_transport import TcpTransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransportFactory:
    '''
        Factory providing polymorphic transport resolution based on port specification.

        It defines:

            :methods:
                | create_transport - Instantiates transport matching target endpoint identifier.
                | create_default_transport - Instantiates default serial transport.
    '''

    @staticmethod
    def create_transport(endpoint: str) -> ITransport:
        '''
            Instantiates transport matching target endpoint identifier.

            :param endpoint: Port device path or host:port socket identifier.
            :return: ITransport instance.
        '''
        if ':' in endpoint:
            return TcpTransport()
        return SerialTransport()

    @staticmethod
    def create_default_transport() -> ITransport:
        '''
            Instantiates default serial transport.

            :return: ITransport instance.
        '''
        return SerialTransport()
