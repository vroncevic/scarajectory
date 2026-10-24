# -*- coding: UTF-8 -*-

'''
Module
    loader.py
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
    Dedicated infrastructure loader for trajectory plan deserialization and file reading.
'''

from __future__ import annotations

from pathlib import Path
from typing import Final

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.serializer.serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanLoader:
    '''
        Infrastructure adapter handling JSON trajectory plan loading and text/binary file reading.

        It defines:

            :attributes:
                | _config_loader - Configuration loader loading JSON structures.
            :methods:
                | __init__ - Initializes the plan loader with configuration loader.
                | load_plan - Loads and deserializes waypoints from JSON file path.
                | load_text_file - Reads string content from file path using UTF-8 encoding.
                | load_binary_file - Reads binary file content from destination file path.
    '''

    _config_loader: IConfigLoader

    def __init__(
        self,
        *,
        config_loader: IConfigLoader,
    ) -> None:
        '''
            Initializes the plan loader with injected configuration loader.

            :param config_loader: IConfigLoader collaborator instance.
        '''
        self._config_loader: Final[IConfigLoader] = config_loader

    def load_plan(self, filepath: str) -> list[TrajectoryWaypoint]:
        '''
            Loads and deserializes waypoints from JSON file path using configuration loader.

            :param filepath: Source file path.
            :return: List of loaded TrajectoryWaypoint instances.
        '''
        target_path: Path = Path(filepath).resolve()

        if not target_path.is_file():
            return []

        data: dict[str, object] = self._config_loader.load(str(target_path))

        return TrajectorySerializer.deserialize_from_dict(data)

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads text content from file path using UTF-8 encoding.

            :param filepath: Source file path.
            :return: File text content string.
        '''
        target_path: Path = Path(filepath).resolve()

        with open(target_path, 'r', encoding='utf-8') as file_handle:
            return file_handle.read()

    def load_binary_file(self, filepath: str) -> bytes:
        '''
            Reads binary file content from file path.

            :param filepath: Source binary file path.
            :return: Raw binary file bytes.
        '''
        target_path: Path = Path(filepath).resolve()

        with open(target_path, 'rb') as file_handle:
            return file_handle.read()
