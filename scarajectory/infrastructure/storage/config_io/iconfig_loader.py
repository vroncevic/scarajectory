# -*- coding: UTF-8 -*-

'''
Module
    iconfig_loader.py
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
    Defines structural protocol IConfigLoader for configuration deserialization.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from ats_utilities.context.bundle import ContextBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IConfigLoader(Protocol):
    '''
        Structural protocol for loading configuration files into dictionary structures.

        It defines:

            :methods:
                | get_context - Retrieves ATS ContextBundle associated with loader.
                | load_configuration - Loads and deserializes configuration content.
    '''

    def get_context(self) -> ContextBundle:
        '''
            Retrieves context bundle associated with this loader.

            :return: ATS ContextBundle instance.
            :exceptions: None.
        '''

    def load_configuration(self) -> dict[str, object]:
        '''
            Loads configuration from file and returns structured dictionary.

            :return: Dictionary containing parsed configuration key-value mappings.
            :exceptions: None.
        '''
