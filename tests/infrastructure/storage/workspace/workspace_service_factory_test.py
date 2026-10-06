# -*- coding: UTF-8 -*-

'''
Module
    workspace_service_factory_test.py
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
    Unit tests for WorkspaceServiceFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.storage.workspace.workspace_constants import WorkspaceConstants
from scarajectory.infrastructure.storage.workspace.workspace_service import WorkspaceService
from scarajectory.infrastructure.storage.workspace.workspace_service_factory import WorkspaceServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceServiceFactory(TestCase):
    '''
        Test cases verifying WorkspaceServiceFactory instantiation.

        It defines:

            :methods:
                | test_create - Verifies factory create method with explicit constants.
                | test_create_default - Verifies factory create_default method.
                | test_get_version - Verifies version string retrieval.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory create method with explicit constants.
        '''
        constants = WorkspaceConstants(workspace_dir='/tmp/custom')
        service = WorkspaceServiceFactory.create(constants=constants)
        self.assertIsInstance(service, WorkspaceService)
        self.assertEqual(service.get_workspace_dir(), '/tmp/custom')

    def test_create_default(self) -> None:
        '''
            Verifies factory create_default method.
        '''
        service = WorkspaceServiceFactory.create_default()
        self.assertIsInstance(service, WorkspaceService)

    def test_get_version(self) -> None:
        '''
            Verifies version string retrieval.
        '''
        version = WorkspaceServiceFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
