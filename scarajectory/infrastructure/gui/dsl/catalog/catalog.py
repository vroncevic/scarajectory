# -*- coding: UTF-8 -*-

'''
Module
    catalog.py
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
    Provides SCARA DSL repository example file catalog access.
'''

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Final

from scarajectory.core.service.storage.iloader import IPlanLoader

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
                | PATTERN_FILE - Glob matching pattern for example scripts.
                | ENCODING - Text file encoding format.
                | EMPTY_CONTENT - Default empty file fallback content.
                | _examples_dir - Filesystem path to bundled examples directory.
                | _loader - Plan storage service for loading example scripts.
            :methods:
                | __init__ - Initializes the catalog with directory and storage service.
                | examples_dir - Returns filesystem path to examples directory.
                | get_example_files - Returns sorted tuple of .scara files in examples directory.
                | load_example_content - Reads and returns content of specified example script.
                | get_version - Returns the component version string.
    '''

    PATTERN_FILE: ClassVar[str] = '*.scara'
    ENCODING: ClassVar[str] = 'utf-8'
    EMPTY_CONTENT: ClassVar[str] = ''

    _examples_dir: Path
    _loader: IPlanLoader

    def __init__(
        self,
        *,
        examples_dir: Path,
        loader: IPlanLoader,
    ) -> None:
        '''
            Initializes the catalog with directory and storage service.

            :param examples_dir: Filesystem path to examples directory.
            :param loader: Plan storage service for loading files.
            :exceptions: None.
        '''
        self._examples_dir: Final[Path] = examples_dir
        self._loader: Final[IPlanLoader] = loader

    def examples_dir(self) -> Path:
        '''
            Returns filesystem path to examples directory.

            :return: Path instance of examples directory.
            :exceptions: None.
        '''
        return self._examples_dir

    def get_example_files(self) -> tuple[str, ...]:
        '''
            Returns sorted tuple of .scara files found in examples directory.

            :return: Tuple of example file names.
            :exceptions: None.
        '''
        if not self._examples_dir.exists():
            return ()
        return tuple(
            p.name for p in sorted(self._examples_dir.glob(self.PATTERN_FILE))
        )

    def load_example_content(self, filename: str) -> str:
        '''
            Reads and returns content of specified example script.

            :param filename: Base name of example file to load.
            :return: Content of example file or empty string if not found.
            :exceptions: None.
        '''
        filepath: Path = self._examples_dir / filename
        if not filepath.exists():
            return self.EMPTY_CONTENT
        try:
            return self._loader.load_text_file(filepath=str(filepath))
        except (OSError, UnicodeDecodeError):
            return self.EMPTY_CONTENT

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component semantic version.
            :exceptions: None.
        '''
        return __version__
