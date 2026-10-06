# -*- coding: UTF-8 -*-

'''
Module
    iconfig_storer.py
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
    Defines structural protocol IConfigStorer for configuration serialization and writing.
'''

from __future__ import annotations

from typing import Any, Mapping, Protocol, runtime_checkable

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
class IConfigStorer(Protocol):
    '''
        Structural protocol for serializing dictionary structures to configuration files.

        It defines:

            :methods:
                | get_context - Retrieves ATS ContextBundle associated with storer.
                | store_configuration - Serializes and writes configuration to destination file.
    '''

    def get_context(self) -> ContextBundle:
        '''
            Retrieves context bundle associated with this storer.

            :return: ATS ContextBundle instance.
            :exceptions: None.
        '''

    def store_configuration(self, config: Mapping[str, Any]) -> bool:
        '''
            Serializes and writes configuration mapping to file.

            :param config: Mapping containing configuration data.
            :return: True if serialization and write succeeded, False otherwise.
            :exceptions: None.
        '''
