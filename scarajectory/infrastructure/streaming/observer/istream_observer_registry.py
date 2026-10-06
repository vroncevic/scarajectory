# -*- coding: UTF-8 -*-

'''
Module
    istream_observer_registry.py
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
    Defines structural protocol IStreamObserverRegistry for observer subscription management.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.service.streaming.observer.iobserver import IObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamObserverRegistry(Protocol):
    '''
    Structural protocol defining streaming observer subscription contracts.

    It defines:

        :methods:
            | set_observer - Sets primary active observer.
            | attach_observer - Registers observer subscriber.
            | detach_observer - Removes observer subscriber.
            | get_observers - Returns snapshot tuple of all registered observers.
    '''

    def set_observer(self, observer: IObserver) -> None:
        '''
        Sets primary active observer.

        :param observer: Non-null IObserver instance.
        '''

    def attach_observer(self, observer: IObserver) -> None:
        '''
        Registers observer subscriber.

        :param observer: Non-null IObserver instance.
        '''

    def detach_observer(self, observer: IObserver) -> None:
        '''
        Removes observer subscriber.

        :param observer: Non-null IObserver instance.
        '''

    def get_observers(self) -> tuple[IObserver, ...]:
        '''
        Returns snapshot tuple of all registered observers.

        :return: Tuple containing registered observers.
        '''
