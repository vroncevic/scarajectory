# -*- coding: UTF-8 -*-

'''
Module
    stream_observer_registry.py
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
    Registry managing stream observer subscriber registration and query.
'''

from __future__ import annotations

from scarajectory.core.service.streaming.observer.iobserver import IObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamObserverRegistry:
    '''
    Registry managing stream observer subscriber registration and query.

    It defines:

        :attributes:
            | _observers - List of registered IObserver subscribers.

        :methods:
            | set_observer - Sets primary active observer.
            | attach_observer - Registers observer subscriber.
            | detach_observer - Removes observer subscriber.
            | get_observers - Returns snapshot tuple of all registered observers.
    '''

    _observers: list[IObserver]

    def __init__(self) -> None:
        '''
        Initializes StreamObserverRegistry with empty observer list.
        '''
        self._observers = []

    def set_observer(self, observer: IObserver) -> None:
        '''
        Sets primary active observer.

        :param observer: Non-null IObserver instance.
        '''
        self._observers = [observer]

    def attach_observer(self, observer: IObserver) -> None:
        '''
        Registers observer subscriber.

        :param observer: Non-null IObserver instance.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def detach_observer(self, observer: IObserver) -> None:
        '''
        Removes observer subscriber.

        :param observer: Non-null IObserver instance.
        '''
        if observer in self._observers:
            self._observers.remove(observer)

    def get_observers(self) -> tuple[IObserver, ...]:
        '''
        Returns snapshot tuple of all registered observers.

        :return: Tuple containing registered observers.
        '''
        return tuple(self._observers)
