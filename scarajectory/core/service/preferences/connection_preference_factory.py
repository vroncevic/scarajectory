# -*- coding: UTF-8 -*-

'''
Module
    connection_preference_factory.py
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
    Factory service constructing ConnectionPreference domain models from parameters or defaults.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.preferences.connection_preference import ConnectionPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionPreferenceFactory:
    '''
        Factory providing creation of ConnectionPreference domain models.

        It defines:

            :attributes:
                | DEFAULT_PORT - Default serial port string identifier.
                | DEFAULT_BAUD - Default serial baud rate frequency integer.
            :methods:
                | create - Constructs ConnectionPreference using explicit parameters.
                | create_default - Constructs ConnectionPreference using sensible defaults.
                | get_version - Returns factory version string.
    '''

    DEFAULT_PORT: Final[str] = '/dev/ttyACM0'
    DEFAULT_BAUD: Final[int] = 115200

    @classmethod
    def create(cls, *, port: str, baud: int) -> ConnectionPreference:
        '''
            Constructs and returns a ConnectionPreference instance with explicit parameters.

            :param port: Communication port path or address string.
            :param baud: Communication baud rate integer.
            :return: Fully configured ConnectionPreference instance.
            :exceptions: None.
        '''
        return ConnectionPreference(port=port, baud=baud)

    @classmethod
    def create_default(cls) -> ConnectionPreference:
        '''
            Constructs and returns a default ConnectionPreference instance.

            :return: Default unconfigured ConnectionPreference instance.
            :exceptions: None.
        '''
        return ConnectionPreference(port=cls.DEFAULT_PORT, baud=cls.DEFAULT_BAUD)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
