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
    Infrastructure storage adapter for trajectory plan serialization and file persistence using ats_utilities.
'''

from __future__ import annotations

from pathlib import Path

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.trajectory.trajectory_serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanStorageService:
    '''
        Infrastructure storage adapter handling JSON trajectory persistence and text file I/O operations.
        Integrates ats_utilities Loader and Storer for JSON configuration management.

        It defines:

            :attributes:
                | _context - The ContextBundle for ATS configuration I/O operations.
            :methods:
                | __init__ - Initializes the plan storage service.
                | save_plan - Saves trajectory plan waypoints to JSON file path using ATS Storer.
                | load_plan - Loads and deserializes waypoints from JSON file path using ATS Loader.
                | save_text_file - Writes string content to file path using UTF-8 encoding.
                | load_text_file - Reads string content from file path using UTF-8 encoding.
    '''

    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle | None = None) -> None:
        '''
            Initializes the plan storage service with optional context bundle.

            :param context_bundle: Optional ATS ContextBundle instance.
        '''
        self._context = context_bundle or ContextBundleFactory.create_bundle()

    def save_plan(self, plan: ITrajectoryPlan, filepath: str) -> None:
        '''
            Saves trajectory plan waypoints to JSON file path using ATS Storer.

            :param plan: ITrajectoryPlan instance.
            :param filepath: Target file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.touch(exist_ok=True)

        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=str(target_path),
                context_bundle=self._context
            )
        )
        storer = Storer(bundle)
        payload: dict[str, object] = TrajectorySerializer.serialize_to_dict(plan.waypoints)
        storer.store_configuration(payload)

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads and deserializes waypoints from JSON file path using ATS Loader.

            :param filepath: Source file path.
            :return: List of loaded Waypoint instances.
        '''
        target_path: Path = Path(filepath).resolve()

        if not target_path.is_file():
            return []

        bundle = ConfigIOBundleFactory.create_bundle(
            ConfigIOBundleOptions(
                file_path=str(target_path),
                context_bundle=self._context
            )
        )
        loader = Loader(bundle)
        data: dict[str, object] = loader.load_configuration()

        return TrajectorySerializer.deserialize_from_dict(data)

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

    def load_text_file(self, filepath: str) -> str:
        '''
            Reads text content from file path using UTF-8 encoding.

            :param filepath: Source file path.
            :return: File text content string.
        '''
        target_path: Path = Path(filepath).resolve()

        with open(target_path, 'r', encoding='utf-8') as file_handle:
            return file_handle.read()
