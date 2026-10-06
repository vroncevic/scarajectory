# -*- coding: UTF-8 -*-

'''
Module
    plan_observer_dispatcher_factory.py
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
    Factory service for creating PlanObserverDispatcher instances.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher import PlanObserverDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanObserverDispatcherFactory:
    '''
        Factory service for creating PlanObserverDispatcher instances.

        It defines:

            :methods:
                | create - Instantiates a new PlanObserverDispatcher.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> PlanObserverDispatcher:
        '''
            Instantiates a new PlanObserverDispatcher.

            :return: New PlanObserverDispatcher instance.
            :exceptions: None.
        '''
        return PlanObserverDispatcher()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
