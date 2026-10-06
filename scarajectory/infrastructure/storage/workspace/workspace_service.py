# -*- coding: UTF-8 -*-

'''
Module
    workspace_service.py
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
    Defines WorkspaceService managing user workspace directory and example script extraction.
'''

from __future__ import annotations

from os import listdir, makedirs
from os.path import exists, expanduser, isdir, join
from tarfile import TarError, TarInfo, open as tar_open
from typing import Final

from scarajectory.infrastructure.storage.workspace.workspace_constants import WorkspaceConstants

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkspaceService:
    '''
        Manages creation, inspection, and examples extraction in the user workspace directory.

        It defines:

            :attributes:
                | _constants - Injected WorkspaceConstants configuration model.
            :methods:
                | __init__ - Initializes workspace service with configuration constants.
                | ensure_workspace - Verifies or creates workspace and extracts examples if absent.
                | get_workspace_dir - Returns expanded absolute workspace directory path.
                | list_scripts - Returns sorted list of .scara scripts in workspace.
                | extract_examples - Unpacks bundled examples archive into user workspace.
    '''

    _constants: WorkspaceConstants

    def __init__(self, constants: WorkspaceConstants) -> None:
        '''
            Initializes WorkspaceService with configuration constants.

            :param constants: Injected WorkspaceConstants configuration model.
            :exceptions: None.
        '''
        self._constants: Final[WorkspaceConstants] = constants

    def get_workspace_dir(self) -> str:
        '''
            Returns expanded absolute workspace path.

            :return: Absolute path string to workspace directory.
            :exceptions: None.
        '''
        return expanduser(self._constants.workspace_dir)

    def list_scripts(self) -> list[str]:
        '''
            Returns sorted list of .scara filenames found in user workspace.

            :return: List of .scara file names.
            :exceptions: None.
        '''
        target_dir: str = self.get_workspace_dir()

        if not exists(target_dir) or not isdir(target_dir):
            return []

        files: list[str] = [
            f for f in listdir(target_dir)
            if f.endswith(self._constants.file_extension)
        ]

        return sorted(files)

    def extract_examples(self, force: bool = False) -> bool:
        '''
            Unpacks examples.tgz archive into user workspace directory.

            :param force: If True, overwrites existing scripts with pristine archive copies.
            :return: True if extraction completed successfully, False otherwise.
            :exceptions: None.
        '''
        if not exists(self._constants.archive_path):
            return False

        target_dir: str = self.get_workspace_dir()
        makedirs(target_dir, exist_ok=True)

        try:
            with tar_open(self._constants.archive_path, self._constants.archive_mode) as tar:
                members: list[TarInfo] = tar.getmembers()

                for member in members:
                    dest_file: str = join(target_dir, member.name)

                    if not exists(dest_file) or force:
                        tar.extract(member, path=target_dir, filter='data')

            return True

        except (TarError, OSError):
            return False

    def ensure_workspace(self) -> str:
        '''
            Ensures user workspace directory exists and extracts examples if missing.

            :return: Absolute expanded path to user workspace directory.
            :exceptions: None.
        '''
        target_dir: str = self.get_workspace_dir()

        if not exists(target_dir):
            makedirs(target_dir, exist_ok=True)

        existing_scripts: list[str] = self.list_scripts()

        if not existing_scripts:
            self.extract_examples(force=False)

        return target_dir
