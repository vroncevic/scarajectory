# -*- coding: UTF-8 -*-

'''
Module
    idelegate.py
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
    Defines structural protocol IDslFileDelegate for script file operations.
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
class IDslFileDelegate(Protocol):
    '''
        Structural protocol defining file opening, saving, and example selection.

        It defines:

            :methods:
                | open_file - Presents open dialog and loads script file into editor.
                | save_file - Presents save dialog and saves editor content to disk.
                | on_example_selected - Loads example script content into editor.
                | get_version - Returns delegate component version string.
    '''

    def open_file(self) -> None:
        '''
            Presents modal open dialog and loads script file into editor.
        '''

    def save_file(self) -> None:
        '''
            Presents modal save dialog and saves editor content to disk.
        '''

    def on_example_selected(self, example_name: str) -> None:
        '''
            Loads specified example script content into editor.

            :param example_name: Base name of example script.
        '''

    def get_version(self) -> str:
        '''
            Returns delegate component version string.

            :return: Semantic version string.
        '''
