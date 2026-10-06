# -*- coding: UTF-8 -*-

'''
Module
    iplan_loader.py
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
    Defines segregated interface IPlanLoader for trajectory plan and file reading operations.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPlanLoader(Protocol):
    '''
        Protocol for loading trajectory plan files and reading text/binary content.

        It defines:

            :methods:
                | load_plan - Loads waypoints from JSON file path.
                | load_text_file - Reads text content from file path.
                | load_binary_file - Reads binary content from file path.
    '''

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads waypoints from JSON file path.

            :param filepath: Source JSON file path.
            :return: List of loaded Waypoint entities.
        '''

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads text content from file path using UTF-8 encoding.

            :param filepath: Source file path.
            :return: File text content string.
        '''

    def load_binary_file(self, filepath: str) -> bytes:
        '''
            Reads binary file content from destination file path.

            :param filepath: Source file path.
            :return: File binary content bytes.
        '''
