# -*- coding: UTF-8 -*-

'''
Module
    iconsole.py
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
    Defines structural protocol IDslConsoleView for diagnostic log console.
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
class IDslConsoleView(Protocol):
    '''
        Structural protocol defining diagnostic log console operations.

        It defines:

            :methods:
                | append_log - Appends message string with syntax-colored level tag.
                | log - Logs message string with success or error color formatting.
                | clear - Clears the console output buffer.
                | get_text - Returns current console buffer content.
                | get_version - Returns console component version string.
    '''

    def append_log(self, text: str, level: str = 'info') -> None:
        '''
            Appends message string with syntax-colored level tag and auto-scrolls.

            :param text: Message string to log.
            :param level: Severity level tag ('info', 'success', 'warning', 'error', 'neutral').
        '''

    def log(self, text: str, is_error: bool = False) -> None:
        '''
            Logs message string with success or error color formatting.

            :param text: Message string to log.
            :param is_error: When True, logs in error style; otherwise in success style.
        '''

    def clear(self) -> None:
        '''
            Clears the console output.
        '''

    def get_text(self) -> str:
        '''
            Returns current console buffer content.

            :return: Console log text.
        '''

    def get_version(self) -> str:
        '''
            Returns console component version string.

            :return: Semantic version string.
        '''
