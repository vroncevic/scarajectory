# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for WorkspaceFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.storage.workspace.config import WorkspaceConfig
from scarajectory.infrastructure.storage.workspace.dependencies import WorkspaceDependencies
from scarajectory.infrastructure.storage.workspace.factory import WorkspaceFactory
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager
from scarajectory.infrastructure.storage.workspace.provides import WorkspaceProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceFactory(TestCase):
    '''
        Test cases verifying WorkspaceFactory instantiation.

        It defines:

            :methods:
                | test_create_with_dependencies - Verifies create with explicit dependencies.
                | test_get_version - Verifies factory version return.
    '''

    def test_create_with_dependencies(self) -> None:
        '''
            Verifies create with explicit dependencies.

            :exceptions: None.
        '''
        config = WorkspaceConfig(workspace_dir='/tmp/custom')
        deps = WorkspaceDependencies(workspace_config=config)
        provides = WorkspaceFactory.create(dependencies=deps)
        self.assertIsInstance(provides, WorkspaceProvides)
        self.assertIsInstance(provides.workspace_manager, IWorkspaceManager)

    def test_get_version(self) -> None:
        '''
            Verifies factory version return.

            :exceptions: None.
        '''
        self.assertEqual(WorkspaceFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
