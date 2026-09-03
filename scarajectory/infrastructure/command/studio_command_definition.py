# -*- coding: UTF-8 -*-

'''
Module
    studio_command_definition.py
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
    Defines StudioCommandDefinition class.
'''

from __future__ import annotations

from collections.abc import Sequence

from ats_utilities.option.command.data import OptionData
from ats_utilities.utils.reflection import to_str

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandDefinition:
    '''
        CLI subcommand metadata definition for SCARAjectory Motion Studio.

        It defines:

            :methods:
                | name - Returns the command name.
                | help_text - Returns the command help text.
                | options - Returns the sequence of command options.
                | __str__ - Returns the command definition as string representation.
    '''

    @property
    def name(self) -> str:
        '''
            Returns the command name.

            :return: The command name.
            :exceptions: None.
        '''
        return 'studio'

    @property
    def help_text(self) -> str:
        '''
            Returns the command help text.

            :return: The command help text.
            :exceptions: None.
        '''
        return 'Run SCARAjectory Motion Studio graphical interface'

    @property
    def options(self) -> Sequence[OptionData]:
        '''
            Returns the command options.

            :return: Sequence of command options.
            :exceptions: None.
        '''
        return [
            OptionData(
                name='--file',
                help_text='Path to initial trajectory JSON plan file',
                action=None,
                default=None,
                required=False,
                choices=None,
                nargs=None
            ),
            OptionData(
                name='--dead-zone',
                help_text='Enable or disable kinematic dead zone enforcement',
                action=None,
                default='enable',
                required=False,
                choices=['enable', 'disable'],
                nargs=None
            ),
            OptionData(
                name='--verbose',
                help_text='Enable or disable verbose output',
                action=None,
                default='disable',
                required=False,
                choices=['enable', 'disable'],
                nargs=None
            )
        ]

    def __str__(self) -> str:
        '''
            Returns the command definition as string representation.

            :return: The command definition as string representation.
            :exceptions: None.
        '''
        return to_str(self)
