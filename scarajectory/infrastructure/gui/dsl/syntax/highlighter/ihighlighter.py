# -*- coding: UTF-8 -*-

'''
Module
    ihighlighter.py
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
    Defines structural protocol IDslSyntaxHighlighter for syntax highlighting coordinator.
'''

from __future__ import annotations

from tkinter import Text
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
class IDslSyntaxHighlighter(Protocol):
    '''
        Structural protocol defining syntax highlighting operations.

        It defines:

            :methods:
                | configure_styles - Configures syntax color tags on widget.
                | highlight - Performs syntax color update on text widget.
                | get_version - Returns syntax highlighter component version string.
    '''

    def configure_styles(self, text_widget: Text) -> None:
        '''
            Configures syntax color tags on the target Tkinter Text widget.

            :param text_widget: Target text widget to format.
        '''

    def highlight(self, text_widget: Text) -> None:
        '''
            Performs complete syntax color update on text widget contents.

            :param text_widget: Target text widget.
        '''

    def get_version(self) -> str:
        '''
            Returns syntax highlighter component version string.

            :return: Semantic version string.
        '''
