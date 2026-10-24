# -*- coding: UTF-8 -*-

'''
Module
    ieditor.py
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
    Defines structural protocol IDslCodeEditor for code editor component.
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
class IDslCodeEditor(Protocol):
    '''
        Structural protocol defining code editor component operations.

        It defines:

            :methods:
                | get_text - Returns full contents of editor buffer.
                | set_text - Replaces editor buffer with provided text.
                | clear - Clears all text in the editor.
                | highlight - Triggers manual syntax highlighting refresh.
                | get_version - Returns editor component version string.
    '''

    def get_text(self) -> str:
        '''
            Returns full contents of the editor buffer.

            :return: Code string.
        '''

    def set_text(self, content: str) -> None:
        '''
            Replaces editor buffer with provided text.

            :param content: Source code string.
        '''

    def clear(self) -> None:
        '''
            Clears all text in the editor.
        '''

    def highlight(self) -> None:
        '''
            Triggers manual syntax highlighting refresh.
        '''

    def get_version(self) -> str:
        '''
            Returns editor component version string.

            :return: Semantic version string.
        '''
