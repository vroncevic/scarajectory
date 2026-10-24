# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for WorkspaceDependencies parameter bundle dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.infrastructure.storage.workspace.config import WorkspaceConfig
from scarajectory.infrastructure.storage.workspace.dependencies import WorkspaceDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceDependencies(TestCase):
    '''
        Test cases verifying WorkspaceDependencies construction and immutability.

        It defines:

            :methods:
                | test_custom_dependencies - Verifies construction with explicit parameters.
                | test_frozen_immutability - Verifies bundle is frozen and immutable.
    '''

    def test_custom_dependencies(self) -> None:
        '''
            Verifies construction with explicit parameters.
        '''
        config = WorkspaceConfig(workspace_dir='/custom/dir')
        deps = WorkspaceDependencies(workspace_config=config)
        self.assertIs(deps.workspace_config, config)
        self.assertEqual(deps.workspace_config.workspace_dir, '/custom/dir')

    def test_frozen_immutability(self) -> None:
        '''
            Verifies bundle is frozen and immutable.
        '''
        deps = WorkspaceDependencies(workspace_config=WorkspaceConfig())
        with self.assertRaises(FrozenInstanceError):
            setattr(deps, 'workspace_config', WorkspaceConfig())


if __name__ == '__main__':
    main()
