# -*- coding: UTF-8 -*-

'''
Module
    jog_command_formatter.py
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
    Manual axis jog step command packet encoder for SCARA microcontroller.
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


class JogCommandFormatter:
    '''
        Formats manual axis jog step commands using template registry.

        It defines:

            :methods:
                | format_jog - Formats manual axis jog step command.
    '''

    @classmethod
    def format_jog(cls, axis: str, step: float) -> str:
        '''
            Formats manual axis jog step command.

            :param axis: Axis name ('X', 'Y', 'Z', 'Phi').
            :param step: Step displacement value in mm or degrees.
            :return: Formatted jog command packet string.
            :exceptions: None.
        '''
        template: str = CommandTemplates.JOG_TEMPLATE

        return template.format(axis=axis.upper(), step=step)
