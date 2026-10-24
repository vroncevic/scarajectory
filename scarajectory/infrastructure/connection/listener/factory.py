# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory service constructing StreamTransportListener instances.
'''

from __future__ import annotations

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.listener.listener import StreamTransportListener
from scarajectory.infrastructure.connection.receiver.ibytes_receiver import IStreamBytesReceiver

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamTransportListenerFactory:
    '''
        Factory providing StreamTransportListener instantiation.

        It defines:

            :methods:
                | create - Constructs StreamTransportListener with receiver and dispatcher.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        dispatcher: IStreamObserverDispatcher,
        bytes_receiver: IStreamBytesReceiver,
    ) -> StreamTransportListener:
        '''
            Constructs and returns a StreamTransportListener instance.

            :param dispatcher: Injected IStreamObserverDispatcher publishing logs.
            :param bytes_receiver: Injected IStreamBytesReceiver processing raw bytes.
            :return: Configured StreamTransportListener instance.
            :exceptions: None.
        '''
        return StreamTransportListener(
            dispatcher=dispatcher,
            bytes_receiver=bytes_receiver,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
