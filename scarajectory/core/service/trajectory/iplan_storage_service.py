# -*- coding: UTF-8 -*-

'''
Module
    iplan_storage_service.py
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
    Defines interface IPlanStorageService for trajectory plan persistence and text file I/O.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPlanStorageService(Protocol):
    '''
        Protocol for storing and loading trajectory plan files and script content.

        It defines:

            :methods:
                | save_plan - Saves current trajectory plan to JSON file path.
                | load_plan - Loads waypoints from JSON file path.
                | save_text_file - Writes text content to file path.
                | load_text_file - Reads text content from file path.
    '''

    def save_plan(self, plan: ITrajectoryPlan, filepath: str) -> None:
        '''
            Saves current trajectory plan to JSON file path.

            :param plan: ITrajectoryPlan instance to save.
            :param filepath: Target JSON file path.
        '''

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads waypoints from JSON file path.

            :param filepath: Source JSON file path.
            :return: List of loaded Waypoint entities.
        '''

    def save_text_file(self, content: str, filepath: str) -> None:
        '''
            Writes text content to file path using UTF-8 encoding.

            :param content: String text to write.
            :param filepath: Destination file path.
        '''

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads text content from file path using UTF-8 encoding.

            :param filepath: Source file path.
            :return: File text content string.
        '''
