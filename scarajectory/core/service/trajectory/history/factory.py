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
    Factory service for creating history navigation and saving instances.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.history.dependencies import HistoryStackDependencies
from scarajectory.core.service.trajectory.history.navigator.dependencies import PlanHistoryNavigatorDependencies
from scarajectory.core.service.trajectory.history.navigator.factory import PlanHistoryNavigatorFactory
from scarajectory.core.service.trajectory.history.navigator.navigator import PlanHistoryNavigator
from scarajectory.core.service.trajectory.history.provides import HistoryStackProvides
from scarajectory.core.service.trajectory.history.saver.dependencies import PlanHistorySaverDependencies
from scarajectory.core.service.trajectory.history.saver.factory import PlanHistorySaverFactory
from scarajectory.core.service.trajectory.history.saver.saver import PlanHistorySaver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanHistoryFactory:
    '''
        Factory service for assembling history subsystem components.

        It defines:

            :methods:
                | create - Assembles history components and returns HistoryStackProvides.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: HistoryStackDependencies) -> HistoryStackProvides:
        '''
            Assembles history components with injected dependencies.

            :param dependencies: Injected HistoryStackDependencies bundle.
            :return: Fully wired HistoryStackProvides instance.
            :exceptions: None.
        '''
        history: PlanHistoryNavigator = PlanHistoryNavigatorFactory.create(
            PlanHistoryNavigatorDependencies(stack=dependencies.stack)
        )
        saver: PlanHistorySaver = PlanHistorySaverFactory.create(
            PlanHistorySaverDependencies(stack=dependencies.stack)
        )

        return HistoryStackProvides(history=history, saver=saver)


    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
