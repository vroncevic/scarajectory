# -*- coding: UTF-8 -*-

'''
Module
    tool_command_formatter.py
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
    End-effector tool, actuator, wait and override command packet encoder.
'''

from __future__ import annotations

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


class ToolCommandFormatter:
    '''
        Formats end-effector tool, dwell wait and feedrate override commands.

        It defines:

            :methods:
                | format_pump - Formats vacuum pump state command.
                | format_valve - Formats release valve state command.
                | format_wait - Formats dwell delay wait command.
                | format_override - Formats feedrate speed override command.
    '''

    @classmethod
    def format_pump(cls, enable: bool) -> str:
        '''
            Formats vacuum pump state command.

            :param enable: True to turn pump on, False for off.
            :return: Formatted pump command packet.
            :exceptions: None.
        '''
        return CommandTemplates.PUMP_ON if enable else CommandTemplates.PUMP_OFF

    @classmethod
    def format_valve(cls, enable: bool) -> str:
        '''
            Formats release valve state command.

            :param enable: True to open valve, False to close.
            :return: Formatted valve command packet.
            :exceptions: None.
        '''
        return CommandTemplates.VALVE_ON if enable else CommandTemplates.VALVE_OFF

    @classmethod
    def format_wait(cls, delay_ms: int) -> str:
        '''
            Formats dwell delay wait command.

            :param delay_ms: Delay in milliseconds.
            :return: Formatted wait command packet.
            :exceptions: None.
        '''
        ms: int = max(0, delay_ms)
        return CommandTemplates.WAIT_TEMPLATE.format(delay_ms=ms)

    @classmethod
    def format_override(cls, percent: int) -> str:
        '''
            Formats feedrate speed override command.

            :param percent: Override percentage (1-200).
            :return: Formatted override command packet.
            :exceptions: None.
        '''
        pct: int = max(1, min(200, percent))
        return CommandTemplates.OVERRIDE_TEMPLATE.format(percent=pct)
