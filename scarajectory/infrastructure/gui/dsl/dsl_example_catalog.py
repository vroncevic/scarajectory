# -*- coding: UTF-8 -*-

'''
Module
    dsl_example_catalog.py
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
    Provides default demonstration SCARA DSL scripts and repository example file catalogs.
'''

from __future__ import annotations

from pathlib import Path
from typing import Final

from scarajectory.core.service.trajectory.iplan_storage_service import (
    IPlanStorageService,
)
from scarajectory.infrastructure.storage.plan_storage_service import (
    PlanStorageService,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DslExampleCatalog:
    '''
        Repository resource provider for SCARA DSL demonstration and example scripts.

        It defines:

            :attributes:
                | _DEFAULT_DEMO_SCRIPT - Hardcoded fallback demonstration script.
                | _examples_dir - Filesystem path to bundled examples directory.
                | _storage - Plan storage service for loading example scripts.
            :methods:
                | __init__ - Initializes the catalog with directory and storage service.
                | get_default_script - Returns standard demonstration SCARA DSL script.
                | get_example_files - Returns sorted list of .scara files found in examples directory.
                | load_example_content - Reads and returns content of specified example script.
    '''

    _DEFAULT_DEMO_SCRIPT: Final[str] = (
        '# ==========================================================\n'
        '# SCARA DSL Industrial Pick & Place Demonstration\n'
        '# ==========================================================\n'
        'CONFIG ELBOW RIGHT\n'
        'SPEED RAPID 120.0\n'
        'SPEED WORK 40.0\n'
        'ACCEL 500.0\n'
        'ZONE BLEND R=5.0\n'
        'TOOL_ORIENT TANGENTIAL\n'
        '\n'
        '# Define sorting pallet grid (3 rows x 4 cols, 20mm pitch)\n'
        'PALLET_DEF TRAY ROWS=3 COLS=4 DX=20.0 DY=20.0\n'
        '\n'
        '# 1. Homing and rapid positioning\n'
        'HOME\n'
        'MOVE_J X=120.0 Y=50.0 Z=20.0 PHI=0.0\n'
        '\n'
        '# 2. Pick & Place arc jump to pallet index 0\n'
        'JUMP X=160.0 Y=80.0 Z=10.0 ARCH=25.0 SPEED=45.0\n'
        'APPROACH DIST=10.0 SPEED=20.0\n'
        'PUMP ON\n'
        'WAIT_MS 100\n'
        'RETRACT DIST=15.0 SPEED=80.0\n'
        '\n'
        '# 3. Transfer to pallet cell 5\n'
        'MOVE_PALLET TRAY INDEX=5 Z=15.0\n'
        'PUMP OFF\n'
        'VALVE ON\n'
        'WAIT_MS 50\n'
        'VALVE OFF\n'
        '\n'
        '# 4. Circular inspection arc\n'
        'ARC_CW X=150.0 Y=40.0 I=0.0 J=-20.0 SPEED=30.0\n'
        'HOME\n'
    )

    _examples_dir: Path
    _storage: IPlanStorageService

    def __init__(
        self,
        *,
        examples_dir: Path | None = None,
        storage: IPlanStorageService | None = None,
    ) -> None:
        '''
            Initializes the catalog with examples directory path and storage service.

            :param examples_dir: Optional filesystem path to examples directory.
            :param storage: Optional IPlanStorageService implementation.
            :exceptions: None.
        '''
        self._examples_dir = (
            examples_dir
            if examples_dir is not None
            else Path(__file__).resolve().parents[4] / 'examples'
        )
        self._storage = (
            storage
            if storage is not None
            else PlanStorageService()
        )

    def get_default_script(self) -> str:
        '''
            Returns the default demonstration SCARA DSL script.

            :return: Multiline script string.
            :exceptions: None.
        '''
        return self._DEFAULT_DEMO_SCRIPT

    def get_example_files(self) -> list[str]:
        '''
            Scans the examples directory and returns a sorted list of .scara filenames.

            :return: Sorted list of filenames.
            :exceptions: None.
        '''
        if not self._examples_dir.is_dir():
            return []

        return sorted(p.name for p in self._examples_dir.glob('*.scara'))

    def load_example_content(self, *, filename: str) -> str | None:
        '''
            Loads and returns the text content of the specified example file.

            :param filename: Name of example script file.
            :return: Text content string or None if file cannot be read.
            :exceptions: None.
        '''
        if not self._examples_dir.is_dir():
            return None
        target_path: Path = self._examples_dir / filename
        if not target_path.is_file():
            return None

        try:
            return self._storage.load_text_file(str(target_path))

        except OSError:
            return None
