# -*- coding: UTF-8 -*-

'''
Module
    iconnection_repository.py
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
    Interface protocol for storing and retrieving hardware communication settings.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.preferences.connection_preference import ConnectionPreference

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IConnectionRepository(Protocol):
    '''
        Storage protocol for persisting and reading hardware connection settings.

        It defines:

            :methods:
                | has_preference - Checks if saved preference configuration exists on disk.
                | load_preference - Reads previously saved connection preference or returns default.
                | save_preference - Persists active connection preference to storage.
    '''

    def has_preference(self) -> bool:
        '''
            Checks if saved preference configuration exists on disk.

            :return: True if preference configuration exists, False otherwise.
        '''

    def load_preference(self) -> ConnectionPreference:
        '''
            Reads previously saved connection preference or returns default.

            :return: ConnectionPreference instance.
        '''

    def save_preference(self, preference: ConnectionPreference) -> bool:
        '''
            Persists active connection preference to storage.

            :param preference: ConnectionPreference instance to persist.
            :return: True if persisted successfully, False otherwise.
        '''
