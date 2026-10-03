# -*- coding: UTF-8 -*-

'''
Module
    isettings_reader.py
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
    Structural protocol defining configuration settings reader contracts.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISettingsReader(Protocol):
    '''
        Structural protocol defining configuration settings reader operations.

        It defines:

            :methods:
                | read_settings - Reads and returns configuration parameters dictionary.
                | get_setting - Retrieves setting value by key with required fallback value.
    '''

    def read_settings(self) -> dict[str, float]:
        '''
            Reads and returns configuration parameters dictionary.

            :return: Dictionary of configuration keys to float values.
        '''

    def get_setting(self, *, key: str, default_val: float) -> float:
        '''
            Retrieves setting value by key with required fallback value.

            :param key: Configuration setting name.
            :param default_val: Fallback numeric value if key is not present.
            :return: Resolved configuration float value.
        '''
