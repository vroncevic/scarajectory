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
    Factory module for assembling SerialPreferenceRepository instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.preferences.serial.dependencies import SerialDependencies
from scarajectory.infrastructure.preferences.serial.provides import SerialProvides
from scarajectory.infrastructure.preferences.serial.repository import SerialPreferenceRepository

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialFactory:
    '''
        Factory responsible for creating SerialPreferenceRepository instances.

        It defines:

            :methods:
                | create - Assembles and instantiates SerialPreferenceRepository wrapped in SerialProvides.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(cls, dependencies: SerialDependencies) -> SerialProvides:
        '''
            Assembles and instantiates SerialPreferenceRepository wrapped in SerialProvides.

            :param dependencies: SerialDependencies instance.
            :return: SerialProvides bundle holding assembled repository.
            :exceptions: None.
        '''
        repo: SerialPreferenceRepository = SerialPreferenceRepository(
            loader=dependencies.config_loader,
            storer=dependencies.config_storer,
            config_file=dependencies.config_file,
        )

        return SerialProvides(serial_preference_repository=repo)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
