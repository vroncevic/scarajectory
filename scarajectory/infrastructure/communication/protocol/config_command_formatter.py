# -*- coding: UTF-8 -*-

'''
Module
    config_command_formatter.py
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
    Configuration command packet encoder for SCARA microcontroller.
'''

from __future__ import annotations

from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.infrastructure.communication.protocol.command_templates import (
    CommandTemplates
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigCommandFormatter:
    '''
        Formats robotic configuration commands using template lookup registry.

        It defines:

            :methods:
                | format_get_config - Formats robot kinematics query command.
                | format_save_config - Formats command persisting config to Flash.
                | format_set_config - Formats configuration update command from ScaraBounds.
    '''

    @classmethod
    def format_get_config(cls) -> str:
        '''
            Formats robot kinematics query command.

            :return: Formatted get config command packet.
            :exceptions: None.
        '''
        return CommandTemplates.GET_CONFIG

    @classmethod
    def format_save_config(cls) -> str:
        '''
            Formats command persisting runtime config to Flash.

            :return: Formatted save config command packet.
            :exceptions: None.
        '''
        return CommandTemplates.SAVE_CONFIG

    @classmethod
    def format_set_config(cls, bounds: ScaraBounds) -> str:
        '''
            Formats configuration update command from ScaraBounds.

            :param bounds: ScaraBounds domain model.
            :return: Formatted set config command packet.
            :exceptions: None.
        '''
        template: str = CommandTemplates.SET_CONFIG_TEMPLATE
        return template.format(
            l1=bounds.l1,
            l2=bounds.l2,
            z_min=bounds.z_min,
            z_max=bounds.z_max,
            min_speed=bounds.min_speed,
            max_speed=bounds.max_speed
        )
