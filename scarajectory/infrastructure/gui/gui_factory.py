# -*- coding: UTF-8 -*-

'''
Module
    gui_factory.py
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
    Factory module for assembling and instantiating ScarajectoryGUI instances.
'''

from __future__ import annotations

from tkinter import Tk

from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.communication.preferences.iconnection_repository import IConnectionRepository
from scarajectory.infrastructure.gui.engine import ScarajectoryGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScarajectoryGUIFactory:
    '''
        Factory responsible for creating ScarajectoryGUI presentation instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a ScarajectoryGUI instance.
                | create_with_root - Assembles a ScarajectoryGUI instance with custom root Tk.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        service: IService,
        connection_repository: IConnectionRepository
    ) -> ScarajectoryGUI:
        '''
            Assembles and instantiates a ScarajectoryGUI instance.

            :param service: IService core logic instance.
            :param connection_repository: Injected IConnectionRepository instance.
            :return: Fully assembled ScarajectoryGUI instance.
            :exceptions: None.
        '''
        return ScarajectoryGUI(
            service=service,
            connection_repository=connection_repository
        )

    @classmethod
    def create_with_root(
        cls,
        *,
        service: IService,
        connection_repository: IConnectionRepository,
        root: Tk
    ) -> ScarajectoryGUI:
        '''
            Assembles and instantiates a ScarajectoryGUI instance with custom root Tk.

            :param service: IService core logic instance.
            :param connection_repository: Injected IConnectionRepository instance.
            :param root: Root Tk window.
            :return: Fully assembled ScarajectoryGUI instance.
            :exceptions: None.
        '''
        return ScarajectoryGUI(
            service=service,
            connection_repository=connection_repository,
            root=root
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__

