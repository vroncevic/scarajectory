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
from scarajectory.core.service.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.gui.igui import IGUI
from scarajectory.infrastructure.cli.icli import ICLI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
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
                | DEPENDENCY_STREAMER - Robot communication streamer key.
                | DEPENDENCY_CLI - CLI adapter key.
                | OPTION_INFO_FILE - Info file configuration key.
                | OPTION_FILE_PATH - Initial plan file path key.
                | OPTION_ROBOT_CONFIG - Custom kinematics configuration file path key.
                | OPTION_L1 - Primary link length key.
                | OPTION_L2 - Secondary link length key.
                | OPTION_Z_MIN - Minimum vertical height limit key.
                | OPTION_Z_MAX - Maximum vertical height limit key.
                | OPTION_MIN_SPEED - Minimum feedrate speed key.
                | OPTION_MAX_SPEED - Maximum feedrate speed key.
            :methods:
                | get_dependency_to_type - Returns mapping of dependencies to types.
                | get_option_to_type - Returns mapping of options to types.
    '''

    DEPENDENCY_BASE: ClassVar[str] = 'base'
    DEPENDENCY_SERVICE: ClassVar[str] = 'service'
    DEPENDENCY_GUI: ClassVar[str] = 'gui'
    DEPENDENCY_STREAMER: ClassVar[str] = 'streamer'
    DEPENDENCY_CLI: ClassVar[str] = 'cli'

    OPTION_INFO_FILE: ClassVar[str] = 'info_file'
    OPTION_FILE_PATH: ClassVar[str] = 'file_path'
    OPTION_ROBOT_CONFIG: ClassVar[str] = 'robot_config'
    OPTION_L1: ClassVar[str] = 'l1'
    OPTION_L2: ClassVar[str] = 'l2'
    OPTION_Z_MIN: ClassVar[str] = 'z_min'
    OPTION_Z_MAX: ClassVar[str] = 'z_max'
    OPTION_MIN_SPEED: ClassVar[str] = 'min_speed'
    OPTION_MAX_SPEED: ClassVar[str] = 'max_speed'

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
            cls.DEPENDENCY_STREAMER: ITrajectoryStreamer,
            cls.DEPENDENCY_CLI: ICLI,
        })

    @classmethod
    def get_option_to_type(cls) -> MappingProxyType[str, type | tuple[type, ...]]:
        '''
            Returns the mapping of bundle options to their expected types.

            :return: MappingProxyType of option keys to types.
            :exceptions: None.
        '''
        return MappingProxyType({
            cls.OPTION_INFO_FILE: str,
            cls.OPTION_FILE_PATH: str,
            cls.OPTION_ROBOT_CONFIG: str,
            cls.OPTION_L1: (int, float),
            cls.OPTION_L2: (int, float),
            cls.OPTION_Z_MIN: (int, float),
            cls.OPTION_Z_MAX: (int, float),
            cls.OPTION_MIN_SPEED: (int, float),
            cls.OPTION_MAX_SPEED: (int, float),
        })
