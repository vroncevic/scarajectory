# -*- coding: UTF-8 -*-

'''
Module
    iworkspace_service.py
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
    Defines structural interface protocol for user workspace initialization and script extraction.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWorkspaceService(Protocol):
    '''
        Defines structural interface protocol for user workspace operations.

        It defines:

            :methods:
                | ensure_workspace - Ensures user workspace directory and unpacks examples.
                | get_workspace_dir - Returns expanded absolute workspace path.
                | list_scripts - Returns sorted list of .scara files in workspace.
                | extract_examples - Unpacks examples.tgz into user workspace directory.
    '''

    def ensure_workspace(self) -> str:
        '''
            Ensures user workspace directory exists and extracts examples if missing.

            :return: Absolute expanded path to user workspace directory.
        '''

    def get_workspace_dir(self) -> str:
        '''
            Returns expanded absolute workspace path.

            :return: Absolute path string to workspace directory.
        '''

    def list_scripts(self) -> list[str]:
        '''
            Returns sorted list of .scara filenames found in user workspace.

            :return: List of .scara file names.
        '''

    def extract_examples(self, force: bool = False) -> bool:
        '''
            Unpacks examples.tgz archive into user workspace directory.

            :param force: If True, overwrites existing scripts with pristine archive copies.
            :return: True if extraction completed successfully, False otherwise.
        '''
