# -*- coding: UTF-8 -*-

'''
Module
    storer.py
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
    Dedicated infrastructure storer for trajectory plan serialization and file writing.
'''

from __future__ import annotations

from pathlib import Path
from typing import Final

from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer
from scarajectory.infrastructure.storage.serializer.serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanStorer:
    '''
        Infrastructure adapter handling JSON trajectory plan saving and text/binary file writing.

        It defines:

            :attributes:
                | _config_storer - Configuration storer persisting JSON structures.
            :methods:
                | __init__ - Initializes the plan storer with configuration storer.
                | save_plan - Saves trajectory plan waypoints to JSON file path.
                | save_text_file - Writes string content to file path using UTF-8 encoding.
                | save_binary_file - Writes compiled binary program payload to destination file path.
    '''

    _config_storer: IConfigStorer

    def __init__(
        self,
        *,
        config_storer: IConfigStorer,
    ) -> None:
        '''
            Initializes the plan storer with injected configuration storer.

            :param config_storer: IConfigStorer collaborator instance.
        '''
        self._config_storer: Final[IConfigStorer] = config_storer

    def save_plan(self, plan: IWaypointQuery, filepath: str) -> None:
        '''
            Saves trajectory plan waypoints to JSON file path using configuration storer.

            :param plan: IWaypointQuery instance.
            :param filepath: Target file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.touch(exist_ok=True)

        payload: dict[str, object] = TrajectorySerializer.serialize_to_dict(
            plan.waypoints
        )
        self._config_storer.store(str(target_path), payload)

    def save_text_file(self, content: str, filepath: str) -> None:
        '''
            Writes text content to file path using UTF-8 encoding.

            :param content: String text to write.
            :param filepath: Destination file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, 'w', encoding='utf-8') as file_handle:
            file_handle.write(content)

    def save_binary_file(self, content: bytes, filepath: str) -> None:
        '''
            Writes compiled binary payload to destination file path.

            :param content: Raw binary bytecode content.
            :param filepath: Destination file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, 'wb') as file_handle:
            file_handle.write(content)
