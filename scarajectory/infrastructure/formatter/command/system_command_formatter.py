# -*- coding: UTF-8 -*-

'''
Module
    system_command_formatter.py
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
    System lifecycle, power, safety and execution control packet encoder for SCARA microcontroller.
'''

from __future__ import annotations

from scarajectory.infrastructure.formatter.command_templates import CommandTemplates

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SystemCommandFormatter:
    '''
        Formats robotic power lifecycle, emergency stop and stream execution control commands.

        It defines:

            :methods:
                | format_enable - Formats motor enable command.
                | format_disable - Formats motor disable command.
                | format_estop - Formats emergency stop command.
                | format_status - Formats status query command.
                | format_pause - Formats streaming pause command.
                | format_resume - Formats streaming resume command.
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
