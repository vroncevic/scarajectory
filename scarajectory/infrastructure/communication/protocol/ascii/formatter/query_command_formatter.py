# -*- coding: UTF-8 -*-

'''
Module
    query_command_formatter.py
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
    Position, kinematic mode and status query command packet encoder for SCARA microcontroller.
'''

from __future__ import annotations

from scarajectory.infrastructure.communication.protocol.ascii.formatter.command_templates import CommandTemplates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueryCommandFormatter:
    '''
        Formats robot state query and kinematic configuration commands.

        It defines:

            :methods:
                | format_getpos - Formats robot current position query command.
                | format_get_elbow - Formats get elbow configuration command.
                | format_set_elbow - Formats set elbow configuration command.
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
    def format_get_elbow(cls) -> str:
        '''
            Formats get elbow configuration command.

            :return: Formatted get elbow command packet string.
            :exceptions: None.
        '''
        return CommandTemplates.GET_ELBOW

    @classmethod
    def format_set_elbow(cls, elbow_left: bool) -> str:
        '''
            Formats set elbow configuration command.

            :param elbow_left: True for Lefty, False for Righty.
            :return: Formatted set elbow command packet string.
            :exceptions: None.
        '''
        name: str = 'LEFT' if elbow_left else 'RIGHT'

        return CommandTemplates.SET_ELBOW_TEMPLATE.format(elbow=name)
