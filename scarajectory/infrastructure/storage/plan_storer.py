# -*- coding: UTF-8 -*-

'''
Module
    plan_storer.py
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

from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from scaralang.core.model.dsl.binary.program import BinaryProgram

from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.infrastructure.storage.trajectory_serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanStorer:
    '''
        Infrastructure adapter handling JSON trajectory plan saving and text/binary file writing.

        It defines:

            :attributes:
                | _context - The ContextBundle for ATS configuration I/O operations.
            :methods:
                | __init__ - Initializes the plan storer with context bundle.
                | save_plan - Saves trajectory plan waypoints to JSON file path using ATS Storer.
                | save_text_file - Writes string content to file path using UTF-8 encoding.
                | save_binary_program - Writes compiled binary program payload to destination file path.
    '''

    _context: ContextBundle

    def __init__(
        self,
        *,
        context_bundle: ContextBundle,
    ) -> None:
        '''
            Initializes the plan storer with injected context bundle.

            :param context_bundle: ATS ContextBundle instance.
        '''
        self._context: Final[ContextBundle] = context_bundle

    def save_plan(self, plan: ITrajectoryReadOnly, filepath: str) -> None:
        '''
            Saves trajectory plan waypoints to JSON file path using ATS Storer.

            :param plan: ITrajectoryReadOnly instance.
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

    def save_binary_program(self, program: BinaryProgram, filepath: str) -> None:
        '''
            Writes compiled binary program payload to destination file path.

            :param program: BinaryProgram instance.
            :param filepath: Destination file path.
        '''
        target_path: Path = Path(filepath).resolve()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, 'wb') as file_handle:
            file_handle.write(program.raw_bytes)
