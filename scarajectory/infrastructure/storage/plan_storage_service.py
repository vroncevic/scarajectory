# -*- coding: UTF-8 -*-

'''
Module
    plan_storage_service.py
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
    Infrastructure storage coordinator delegating trajectory plan loading and storing.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.storage.iplan_loader import IPlanLoader
from scarajectory.core.service.storage.iplan_storer import IPlanStorer
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanStorageService:
    '''
        Infrastructure storage adapter coordinating JSON trajectory persistence and file I/O operations.

        It defines:

            :attributes:
                | _loader - Dedicated plan and file reader collaborator.
                | _storer - Dedicated plan and file writer collaborator.
            :methods:
                | __init__ - Initializes the plan storage service with injected loader and storer.
                | save_plan - Saves trajectory plan waypoints to JSON file path.
                | load_plan - Loads and deserializes waypoints from JSON file path.
                | save_text_file - Writes string content to file path using UTF-8 encoding.
                | load_text_file - Reads string content from file path using UTF-8 encoding.
                | save_binary_program - Writes compiled binary program payload to destination file path.
                | load_binary_file - Reads binary file content from destination file path.
    '''

    _loader: IPlanLoader
    _storer: IPlanStorer

    def __init__(self, loader: IPlanLoader, storer: IPlanStorer) -> None:
        '''
            Initializes the plan storage service with injected loader and storer.

            :param loader: Injected IPlanLoader collaborator.
            :param storer: Injected IPlanStorer collaborator.
        '''
        self._loader: Final[IPlanLoader] = loader
        self._storer: Final[IPlanStorer] = storer

    def save_plan(self, plan: ITrajectoryReadOnly, filepath: str) -> None:
        '''
            Saves trajectory plan waypoints to JSON file path.

            :param plan: ITrajectoryReadOnly instance.
            :param filepath: Target file path.
        '''
        self._storer.save_plan(plan, filepath)

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads and deserializes waypoints from JSON file path.

            :param filepath: Source file path.
            :return: List of loaded Waypoint instances.
        '''
        return self._loader.load_plan(filepath)

    def save_text_file(self, content: str, filepath: str) -> None:
        '''
            Writes text content to file path using UTF-8 encoding.

            :param content: String text to write.
            :param filepath: Destination file path.
        '''
        self._storer.save_text_file(content, filepath)

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads text content from file path using UTF-8 encoding.

            :param filepath: Source file path.
            :return: File text content string.
        '''
        return self._loader.load_text_file(filepath)

    def save_binary_program(self, program: BinaryProgram, filepath: str) -> None:
        '''
            Writes compiled binary program payload to destination file path.

            :param program: BinaryProgram instance.
            :param filepath: Destination file path.
        '''
        self._storer.save_binary_program(program, filepath)

    def load_binary_file(self, filepath: str) -> bytes:
        '''
            Reads binary file content from file path.

            :param filepath: Source file path.
            :return: File bytes content.
        '''
        return self._loader.load_binary_file(filepath)
