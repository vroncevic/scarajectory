# -*- coding: UTF-8 -*-

'''
Module
    plan_observer_dispatcher.py
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
    Concrete implementation of trajectory plan observer dispatcher.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.plan.observer.itrajectory_observer import ITrajectoryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanObserverDispatcher:
    '''
        Concrete implementation of trajectory plan observer dispatcher.

        It defines:

            :attributes:
                | _observers - List of registered observer listeners.
            :methods:
                | __init__ - Initializes empty dispatcher.
                | count - Returns number of registered observers.
                | add_observer - Registers an observer for change notifications.
                | remove_observer - Unregisters an observer from notifications.
                | notify_change - Notifies all registered observers on trajectory change.
    '''

    _observers: list[ITrajectoryObserver]

    def __init__(self) -> None:
        '''
            Initializes an empty observer dispatcher.

            :exceptions: None.
        '''
        self._observers = []

    @property
    def count(self) -> int:
        '''
            Returns number of registered observers.

            :return: Integer observer count.
            :exceptions: None.
        '''
        return len(self._observers)

    def add_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Registers an observer for change notifications.

            :param observer: ITrajectoryObserver instance.
            :exceptions: None.
        '''
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Unregisters an observer from notifications.

            :param observer: ITrajectoryObserver instance.
            :exceptions: None.
        '''
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_change(self) -> None:
        '''
            Notifies all registered observers on trajectory change.

            :exceptions: None.
        '''
        for obs in self._observers:
            if hasattr(obs, 'on_trajectory_updated'):
                obs.on_trajectory_updated()
            elif hasattr(obs, 'on_plan_changed'):
                obs.on_plan_changed()
