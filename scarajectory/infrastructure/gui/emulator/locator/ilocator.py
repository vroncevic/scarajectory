# -*- coding: UTF-8 -*-

'''
Module
    ilocator.py
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
    Defines interface IEmulatorLocator for discovering and configuring SCARAEmu executable.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IEmulatorLocator(Protocol):
    '''
        Protocol defining contract for external SCARAEmu path discovery and command generation.

        It defines:

            :methods:
                | is_available - Checks if external emulator executable or script is available.
                | build_command - Builds executable command list for spawning emulator process.
                | build_environment - Builds environment dictionary for external process.
                | get_version - Returns locator interface version string.
    '''

    def is_available(self) -> bool:
        '''
            Checks if external emulator executable or script is available.

            :return: True if available, False otherwise.
        '''

    def build_command(self, *, file_path: str) -> list[str]:
        '''
            Builds executable command list for spawning emulator process.

            :param file_path: Path to trajectory plan file to preview.
            :return: Subprocess command arguments list.
        '''

    def build_environment(self) -> dict[str, str]:
        '''
            Builds environment dictionary for external process.

            :return: Environment variables mapping.
        '''

    def get_version(self) -> str:
        '''
            Returns the locator interface version string.

            :return: Version string.
        '''
