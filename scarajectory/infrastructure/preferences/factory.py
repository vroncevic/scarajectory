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
    Factory module for assembling preferences subsystem.
'''

from __future__ import annotations

from scarajectory.infrastructure.preferences.dependencies import PreferencesDependencies
from scarajectory.infrastructure.preferences.provides import PreferencesProvides
from scarajectory.infrastructure.preferences.serial.dependencies import SerialDependencies
from scarajectory.infrastructure.preferences.serial.factory import SerialFactory
from scarajectory.infrastructure.preferences.serial.provides import SerialProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PreferencesFactory:
    '''
        Factory responsible for assembling preferences subsystem.

        It defines:

            :methods:
                | create - Assembles and wires preferences subsystem returning PreferencesProvides.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(cls, dependencies: PreferencesDependencies) -> PreferencesProvides:
        '''
            Assembles and wires preferences subsystem returning PreferencesProvides.

            :param dependencies: PreferencesDependencies instance.
            :return: PreferencesProvides container holding preference repositories.
            :exceptions: None.
        '''
        serial_provides: SerialProvides = SerialFactory.create(
            SerialDependencies(
                config_loader=dependencies.config_loader,
                config_storer=dependencies.config_storer,
                config_file=dependencies.serial_config_file,
            )
        )

        return PreferencesProvides(
            serial_repository=serial_provides.serial_preference_repository
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
