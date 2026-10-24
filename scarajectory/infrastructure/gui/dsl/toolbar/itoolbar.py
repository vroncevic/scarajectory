# -*- coding: UTF-8 -*-

'''
Module
    itoolbar.py
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
    Defines structural protocol IDslEditorToolbar for editor action toolbar.
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
class IDslEditorToolbar(Protocol):
    '''
        Structural protocol defining toolbar subcomponent operations.

        It defines:

            :methods:
                | handle_example_change - Handles selection event on example dropdown.
                | get_selected_example - Returns the name of currently selected example.
                | set_selected_example - Sets the active example name in dropdown.
                | set_example_files - Populates example choices in dropdown.
                | get_version - Returns toolbar component version string.
    '''

    def handle_example_change(self, _event: object = '') -> None:
        '''
            Handles selection event on example dropdown.

            :param _event: Optional Tkinter event.
        '''

    def get_selected_example(self) -> str:
        '''
            Returns the name of the currently selected example script.

            :return: String filename of example script.
        '''

    def set_selected_example(self, name: str) -> None:
        '''
            Sets the active example name in the dropdown.

            :param name: Filename to select.
        '''

    def set_example_files(self, files: list[str]) -> None:
        '''
            Populates example choices in dropdown.

            :param files: List of available example filenames.
        '''

    def get_version(self) -> str:
        '''
            Returns toolbar component version string.

            :return: Semantic version string.
        '''
