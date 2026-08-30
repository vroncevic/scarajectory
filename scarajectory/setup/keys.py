# -*- coding: UTF-8 -*-

'''
Module
    keys.py
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
    Runtime components and interface constraints for the scarajectory bundle.
'''

from __future__ import annotations

from typing import ClassVar
from types import MappingProxyType

from ats_utilities.base.setup.bundle import BaseBundle

from scarajectory.core.service.iservice import IService
from scarajectory.core.service.iserial_streamer import ISerialStreamer
from scarajectory.infrastructure.gui.igui import IGUI

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SCARAjectoryBundleKeys:
    '''
        Runtime components and interface constraints for the scarajectory bundle.

        It defines:

            :attributes:
                | DEPENDENCY_BASE - Base bundle key.
                | DEPENDENCY_SERVICE - Service key.
                | DEPENDENCY_GUI - GUI adapter key.
                | DEPENDENCY_STREAMER - Serial streamer key.
                | OPTION_INFO_FILE - Info file configuration key.
                | OPTION_FILE_PATH - Initial plan file path key.
            :methods:
                | get_dependency_to_type - Returns mapping of dependencies to types.
                | get_option_to_type - Returns mapping of options to types.
    '''

    DEPENDENCY_BASE: ClassVar[str] = 'base'
    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_GUI: ClassVar[str] = 'gui'
    DEPENDENCY_STREAMER: ClassVar[str] = 'streamer'

    OPTION_INFO_FILE: ClassVar[str] = 'info_file'
    OPTION_FILE_PATH: ClassVar[str] = 'file_path'

    @classmethod
    def get_dependency_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of bundle dependencies to their expected types.

            :return: MappingProxyType of dependency keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.DEPENDENCY_BASE: BaseBundle,
            cls.DEPENDENCY_SERVICE: IService,
            cls.DEPENDENCY_GUI: IGUI,
            cls.DEPENDENCY_STREAMER: ISerialStreamer,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type]:
        '''
            Returns the mapping of bundle options to their expected types.

            :return: MappingProxyType of option keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_INFO_FILE: str,
            cls.OPTION_FILE_PATH: str,
        })
