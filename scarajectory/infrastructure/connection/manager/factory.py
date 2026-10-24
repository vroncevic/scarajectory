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
    Factory service constructing configured ManagerProvides instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.connection.manager.dependencies import ManagerDependencies
from scarajectory.infrastructure.connection.manager.manager import ConnectionManager
from scarajectory.infrastructure.connection.manager.provides import ManagerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManagerFactory:
    '''
        Factory providing creation of ManagerProvides instances.

        It defines:

            :methods:
                | create - Constructs and returns a ManagerProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ManagerDependencies) -> ManagerProvides:
        '''
            Constructs and returns a ManagerProvides instance with injected dependencies.

            :param dependencies: Injected ManagerDependencies bundle.
            :return: ManagerProvides instance.
            :exceptions: None.
        '''
        manager = ConnectionManager(
            connection_coordinator=dependencies.connection_coordinator
        )

        return ManagerProvides(connection_manager=manager)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
