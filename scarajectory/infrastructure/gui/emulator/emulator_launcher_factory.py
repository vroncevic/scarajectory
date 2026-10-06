# -*- coding: UTF-8 -*-

'''
Module
    emulator_launcher_factory.py
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
    Factory module for creating EmulatorLauncher instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.emulator.emulator_launcher import EmulatorLauncher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorLauncherFactory:
    '''
        Factory providing EmulatorLauncher instances.

        It defines:

            :methods:
                | create - Constructs a new EmulatorLauncher instance.
                | get_version - Returns the version of the factory.
    '''

    @classmethod
    def create(cls) -> EmulatorLauncher:
        '''
            Constructs a new EmulatorLauncher instance.

            :return: EmulatorLauncher instance.
            :exceptions: None.
        '''
        return EmulatorLauncher()

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the version of the factory.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
