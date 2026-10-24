# -*- coding: UTF-8 -*-

'''
Module
    config_test.py
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
    Unit tests for WorkspaceConfig data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from os.path import exists
from unittest import TestCase, main

from scarajectory.infrastructure.storage.workspace.config import WorkspaceConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceConfig(TestCase):
    '''
        Test cases verifying WorkspaceConfig configuration behavior.

        It defines:

            :methods:
                | test_default_config - Tests default values and bundled archive path.
                | test_custom_config - Tests construction with custom field values.
                | test_frozen_immutability - Verifies that config instances cannot be mutated.
    '''

    def test_default_config(self) -> None:
        '''
            Tests default values and bundled archive path existence.
        '''
        config = WorkspaceConfig()
        self.assertEqual(config.workspace_dir, '~/.scarajectory/workspace')
        self.assertEqual(config.archive_mode, 'r:gz')
        self.assertEqual(config.file_extension, '.scara')
        self.assertTrue(exists(config.archive_path))

    def test_custom_config(self) -> None:
        '''
            Tests construction with custom field values.
        '''
        config = WorkspaceConfig(
            workspace_dir='/tmp/custom_scara',
            archive_path='/tmp/custom.tgz',
            archive_mode='r',
            file_extension='.txt',
        )
        self.assertEqual(config.workspace_dir, '/tmp/custom_scara')
        self.assertEqual(config.archive_path, '/tmp/custom.tgz')
        self.assertEqual(config.archive_mode, 'r')
        self.assertEqual(config.file_extension, '.txt')

    def test_frozen_immutability(self) -> None:
        '''
            Verifies that config instances cannot be mutated.
        '''
        config = WorkspaceConfig()
        with self.assertRaises(FrozenInstanceError):
            setattr(config, 'workspace_dir', '/tmp/forbidden')


if __name__ == '__main__':
    main()
