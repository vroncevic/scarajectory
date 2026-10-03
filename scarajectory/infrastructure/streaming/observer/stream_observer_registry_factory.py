# -*- coding: UTF-8 -*-

'''
Module
    stream_observer_registry_factory.py
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
    Factory service constructing StreamObserverRegistry instances.
'''

from __future__ import annotations

from scarajectory.core.service.streaming.observer.iobserver import IObserver
from scarajectory.infrastructure.streaming.observer.stream_observer_registry import StreamObserverRegistry

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverRegistryFactory:
    '''
    Factory providing creation of StreamObserverRegistry instances.

    It defines:

        :methods:
            | create - Constructs StreamObserverRegistry instance.
            | create_with_observer - Constructs registry with explicit initial observer.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> StreamObserverRegistry:
        '''
        Constructs a fresh StreamObserverRegistry instance with zero initial observers.

        :return: StreamObserverRegistry instance.
        '''
        return StreamObserverRegistry()

    @classmethod
    def create_with_observer(
        cls,
        observer: IObserver,
    ) -> StreamObserverRegistry:
        '''
        Constructs a fresh StreamObserverRegistry instance with explicit initial observer.

        :param observer: Explicit non-null IObserver instance.
        :return: StreamObserverRegistry instance.
        '''
        registry = StreamObserverRegistry()
        registry.set_observer(observer)
        return registry

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Factory version string.
        '''
        return __version__
