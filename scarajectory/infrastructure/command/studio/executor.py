# -*- coding: UTF-8 -*-

'''
Module
    executor.py
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
    Defines StudioCommandExecutor class.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from ats_utilities.utils.reflection import to_str

from scarajectory.infrastructure.command.idefinition import ICommandDefinition
from scarajectory.infrastructure.gui.igui import IGUI

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioCommandExecutor:
    '''
        Command executor strategy for launching SCARAjectory Motion Studio GUI.

        It defines:

            :attributes:
                | _definition - The command CLI metadata definition.
                | _gui - The GUI presentation adapter instance.
            :methods:
                | __init__ - Initializes the command executor.
                | execute - Executes the studio command.
                | get_definition - Returns the command definition metadata.
                | __str__ - Returns the StudioCommandExecutor as string representation.
    '''

    _definition: ICommandDefinition
    _gui: IGUI

    def __init__(self, *, definition: ICommandDefinition, gui: IGUI) -> None:
        '''
            Initializes the command executor.

            :param definition: The command definition metadata.
            :param gui: The GUI presentation adapter instance.
            :exceptions: None.
        '''
        self._definition: Final[ICommandDefinition] = definition
        self._gui: Final[IGUI] = gui

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: object,
    ) -> Mapping[str, object]:
        '''
            Executes the subcommand.

            :param params: Subcommand parameters from CLI parser.
            :param service: Contextual service parameter.
            :return: The result of the subcommand execution.
            :exceptions: None.
        '''

        _ = service
        if not self._gui.is_initialized():
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': 'studio_command_executor::execute - gui not initialized',
            }

        try:
            file_path: object = params.get('file')

            if isinstance(file_path, str) and file_path.strip():
                self._gui.load_file(file_path)

            if bool(params.get('dead_zone')):
                self._gui.set_deadzone(True)

            self._gui.start()

            return {
                'returncode': 0,
                'stdout': 'Studio closed successfully',
                'stderr': '',
            }

        except Exception as exc:
            return {
                'returncode': 1,
                'stdout': '',
                'stderr': f'studio_command_executor::execute - {exc}',
            }

    def get_definition(self) -> ICommandDefinition:
        '''
            Returns the command definition metadata.

            :return: The command definition metadata.
            :exceptions: None.
        '''
        return self._definition

    def __str__(self) -> str:
        '''
            Returns the StudioCommandExecutor as string representation.

            :return: The StudioCommandExecutor as string representation.
            :exceptions: None.
        '''
        return to_str(self)
