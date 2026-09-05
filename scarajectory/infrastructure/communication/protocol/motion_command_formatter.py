# -*- coding: UTF-8 -*-

'''
Module
    motion_command_formatter.py
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
    Motion and runtime command packet encoder for SCARA microcontroller.
'''

from __future__ import annotations

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.infrastructure.communication.protocol.command_templates import (
    CommandTemplates
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandFormatter:
    '''
        Formats robotic motion and runtime control commands using template registry.

        It defines:

            :methods:
                | format_getpos - Formats robot current position query command.
                | format_enable - Formats motor enable command.
                | format_disable - Formats motor disable command.
                | format_estop - Formats emergency stop command.
                | format_status - Formats status query command.
                | format_pause - Formats streaming pause command.
                | format_resume - Formats streaming resume command.
                | format_home - Formats homing sequence command.
                | format_move - Formats waypoint motion command from Waypoint model.
                | format_jog - Formats manual axis jog step command.
                | format_set_elbow - Formats set elbow configuration command.
                | format_get_elbow - Formats get elbow configuration command.
    '''

    @classmethod
    def format_getpos(cls) -> str:
        '''
            Formats position query command.

            :return: Formatted position query command string.
            :exceptions: None.
        '''
        return CommandTemplates.GETPOS

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
    def format_set_elbow(cls, elbow_left: bool) -> str:
        '''
            Formats set elbow configuration command.

            :param elbow_left: True for Lefty, False for Righty.
            :return: Formatted set elbow command packet.
            :exceptions: None.
        '''
        name: str = 'LEFT' if elbow_left else 'RIGHT'
        return CommandTemplates.SET_ELBOW_TEMPLATE.format(elbow=name)

    @classmethod
    def format_get_elbow(cls) -> str:
        '''
            Formats get elbow configuration command.

            :return: Formatted get elbow command packet.
            :exceptions: None.
        '''
        return CommandTemplates.GET_ELBOW
