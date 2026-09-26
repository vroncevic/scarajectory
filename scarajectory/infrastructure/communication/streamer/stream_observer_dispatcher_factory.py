# -*- coding: UTF-8 -*-

'''
Module
    stream_observer_dispatcher_factory.py
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
    Factory service constructing StreamObserverDispatcher instances.
'''

from __future__ import annotations

from scarajectory.core.service.communication.stream.iobserver import IObserver
from scarajectory.infrastructure.communication.streamer.stream_observer_dispatcher import StreamObserverDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverDispatcherFactory:
    '''
        Factory providing creation of StreamObserverDispatcher instances.

        It defines:

            :methods:
                | create - Constructs an empty StreamObserverDispatcher.
                | create_with_observer - Constructs StreamObserverDispatcher with registered observer.
    '''

    @classmethod
    def create(cls) -> StreamObserverDispatcher:
        '''
            Constructs and returns an empty StreamObserverDispatcher instance.

            :return: StreamObserverDispatcher instance.
        '''
        return StreamObserverDispatcher()

    @classmethod
    def create_with_observer(cls, observer: IObserver) -> StreamObserverDispatcher:
        '''
            Constructs and returns a StreamObserverDispatcher configured with an observer.

            :param observer: IObserver instance.
            :return: StreamObserverDispatcher instance.
        '''
        return StreamObserverDispatcher(observer=observer)

