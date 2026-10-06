# -*- coding: UTF-8 -*-

'''
Module
    plan_loader.py
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

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_loader import IConfigLoader
from scarajectory.infrastructure.storage.trajectory_serializer import TrajectorySerializer

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
                | _io_factory - Configuration I/O factory constructing loaders.
            :methods:
                | __init__ - Initializes the plan loader with I/O factory.
                | load_plan - Loads and deserializes waypoints from JSON file path.
                | load_text_file - Reads string content from file path using UTF-8 encoding.
                | load_binary_file - Reads binary file content from destination file path.
    '''

    _io_factory: IConfigIOFactory

    def __init__(
        self,
        *,
        io_factory: IConfigIOFactory,
    ) -> None:
        '''
            Initializes the plan loader with injected configuration I/O factory.

            :param io_factory: IConfigIOFactory instance.
        '''
        self._io_factory: Final[IConfigIOFactory] = io_factory

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads and deserializes waypoints from JSON file path using configuration loader.

            :param filepath: Source file path.
            :return: List of loaded Waypoint instances.
        '''
        target_path: Path = Path(filepath).resolve()

        if not target_path.is_file():
            return []

        loader: IConfigLoader = self._io_factory.create_loader(str(target_path))
        data: dict[str, object] = loader.load_configuration()

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

            :param filepath: Source file path.
            :return: File bytes content.
        '''
        target_path: Path = Path(filepath).resolve()

        with open(target_path, 'rb') as file_handle:
            return file_handle.read()
