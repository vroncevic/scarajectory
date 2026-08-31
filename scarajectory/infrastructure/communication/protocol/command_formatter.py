# -*- coding: UTF-8 -*-

'''
Module
    command_formatter.py
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
    Formats and interpolates robotic commands using template lookup registry.
'''

from __future__ import annotations

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.infrastructure.communication.protocol.command_templates import CommandTemplates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFormatter:
    '''
        Formats and interpolates robotic commands using template lookup registry.

        It defines:

            :methods:
                | format_enable - Formats motor enable command.
                | format_disable - Formats motor disable command.
                | format_estop - Formats emergency stop command.
                | format_status - Formats status query command.
                | format_pause - Formats streaming pause command.
                | format_resume - Formats streaming resume command.
                | format_home - Formats homing sequence command.
                | format_pump - Formats vacuum pump state command.
                | format_valve - Formats release valve state command.
                | format_move - Formats waypoint motion command from Waypoint model.
                | format_jog - Formats manual axis jog step command.
                | format_get_config - Formats robot kinematics query command.
                | format_save_config - Formats command persisting config to Flash.
                | format_set_config - Formats configuration update command from ScaraBounds.
    '''

    @classmethod
    def format_enable(cls) -> str:
        '''
            Formats motor enable command.

            :return: Formatted enable command string.
            :exceptions: None.
        '''
        return CommandTemplates.ENABLE

    @classmethod
    def format_disable(cls) -> str:
        '''
            Formats motor disable command.

            :return: Formatted disable command string.
            :exceptions: None.
        '''
        return CommandTemplates.DISABLE

    @classmethod
    def format_estop(cls) -> str:
        '''
            Formats emergency stop command.

            :return: Formatted emergency stop command string.
            :exceptions: None.
        '''
        return CommandTemplates.ESTOP

    @classmethod
    def format_status(cls) -> str:
        '''
            Formats status query command.

            :return: Formatted status query command string.
            :exceptions: None.
        '''
        return CommandTemplates.STATUS

    @classmethod
    def format_pause(cls) -> str:
        '''
            Formats streaming pause command.

            :return: Formatted pause command string.
            :exceptions: None.
        '''
        return CommandTemplates.PAUSE

    @classmethod
    def format_resume(cls) -> str:
        '''
            Formats streaming resume command.

            :return: Formatted resume command string.
            :exceptions: None.
        '''
        return CommandTemplates.RESUME

    @classmethod
    def format_home(cls) -> str:
        '''
            Formats homing sequence command.

            :return: Formatted home command string.
            :exceptions: None.
        '''
        return CommandTemplates.HOME

    @classmethod
    def format_pump(cls, state: bool) -> str:
        '''
            Formats vacuum pump control command.

            :param state: True for pump ON, False for OFF.
            :return: Formatted pump command string.
            :exceptions: None.
        '''
        return CommandTemplates.PUMP_ON if state else CommandTemplates.PUMP_OFF

    @classmethod
    def format_valve(cls, state: bool) -> str:
        '''
            Formats release valve control command.

            :param state: True for valve ON, False for OFF.
            :return: Formatted valve command string.
            :exceptions: None.
        '''
        return CommandTemplates.VALVE_ON if state else CommandTemplates.VALVE_OFF

    @classmethod
    def format_move(cls, waypoint: Waypoint) -> str:
        '''
            Formats waypoint motion command from Waypoint model.

            :param waypoint: Waypoint domain object.
            :return: Formatted move command packet.
            :exceptions: None.
        '''
        template: str = CommandTemplates.MOVE_TEMPLATE
        return template.format(
            x=waypoint.x,
            y=waypoint.y,
            z=waypoint.z,
            phi=waypoint.phi,
            speed=waypoint.speed
        )

    @classmethod
    def format_jog(cls, axis: str, step: float) -> str:
        '''
            Formats manual axis jog step command.

            :param axis: Axis name ('X', 'Y', 'Z', 'Phi').
            :param step: Step displacement value.
            :return: Formatted jog command packet.
            :exceptions: None.
        '''
        template: str = CommandTemplates.JOG_TEMPLATE
        return template.format(axis=axis.upper(), step=step)

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
