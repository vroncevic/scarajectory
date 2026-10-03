# -*- coding: UTF-8 -*-

'''
Module
    transport_reader_worker_factory.py
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
    Factory service constructing TransportReaderWorker instances.
'''

from __future__ import annotations

from threading import Event

from scarajectory.infrastructure.transport.driver.ichannel import IChannelDriver
from scarajectory.infrastructure.transport.listener.itransport_listener import ITransportListener
from scarajectory.infrastructure.transport.worker.transport_reader_worker import TransportReaderWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransportReaderWorkerFactory:
    '''
        Factory providing creation of TransportReaderWorker instances.

        It defines:

            :methods:
                | create - Constructs TransportReaderWorker with synchronization event, driver, and listener.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        stop_event: Event,
        driver: IChannelDriver,
        listener: ITransportListener,
    ) -> TransportReaderWorker:
        '''
            Constructs and returns TransportReaderWorker instance.

            :param stop_event: Event signaling termination request.
            :param driver: Injected IChannelDriver instance.
            :param listener: Injected ITransportListener instance.
            :return: TransportReaderWorker instance.
            :exceptions: None.
        '''
        return TransportReaderWorker(
            stop_event=stop_event,
            driver=driver,
            listener=listener,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
