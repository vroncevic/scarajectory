# -*- coding: UTF-8 -*-

'''
Module
    workspace_service_test.py
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
    Unit tests for WorkspaceService component.
'''

from __future__ import annotations

from os.path import exists, expanduser, join
from tarfile import TarError
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import patch

from scarajectory.infrastructure.storage.workspace.workspace_constants import WorkspaceConstants
from scarajectory.infrastructure.storage.workspace.workspace_service import WorkspaceService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceService(TestCase):
    '''
        Test cases verifying WorkspaceService operations.

        It defines:

            :methods:
                | test_get_workspace_dir - Verifies expansion of home directory path.
                | test_list_scripts_missing_or_not_dir - Verifies list_scripts on non-existent directory.
                | test_list_scripts_populated - Verifies list_scripts returns sorted matching files.
                | test_extract_examples_missing_archive - Verifies extraction returns False on missing archive.
                | test_extract_examples_success_and_force - Verifies archive unpacking into target directory.
                | test_extract_examples_tar_error - Verifies error handling on archive decompression fault.
                | test_ensure_workspace_missing_and_existing - Verifies directory creation and script check.
    '''

    def test_get_workspace_dir(self) -> None:
        '''
            Verifies expansion of home directory path.
        '''
        constants = WorkspaceConstants(workspace_dir='~/test_workspace')
        service = WorkspaceService(constants=constants)
        self.assertEqual(service.get_workspace_dir(), expanduser('~/test_workspace'))

    def test_list_scripts_missing_or_not_dir(self) -> None:
        '''
            Verifies list_scripts on non-existent directory or regular file.
        '''
        with TemporaryDirectory() as tmp_dir:
            missing_dir: str = join(tmp_dir, 'does_not_exist')
            service = WorkspaceService(constants=WorkspaceConstants(workspace_dir=missing_dir))
            self.assertEqual(service.list_scripts(), [])

            file_path: str = join(tmp_dir, 'not_a_dir')
            with open(file_path, 'w', encoding='utf-8') as handle:
                handle.write('test')

            service_file = WorkspaceService(constants=WorkspaceConstants(workspace_dir=file_path))
            self.assertEqual(service_file.list_scripts(), [])

    def test_list_scripts_populated(self) -> None:
        '''
            Verifies list_scripts returns sorted matching files.
        '''
        with TemporaryDirectory() as tmp_dir:
            with open(join(tmp_dir, 'b_test.scara'), 'w', encoding='utf-8') as handle:
                handle.write('HOME')
            with open(join(tmp_dir, 'a_test.scara'), 'w', encoding='utf-8') as handle:
                handle.write('HOME')
            with open(join(tmp_dir, 'ignore.txt'), 'w', encoding='utf-8') as handle:
                handle.write('TEXT')

            service = WorkspaceService(constants=WorkspaceConstants(workspace_dir=tmp_dir))
            self.assertEqual(service.list_scripts(), ['a_test.scara', 'b_test.scara'])

    def test_extract_examples_missing_archive(self) -> None:
        '''
            Verifies extraction returns False when archive path does not exist.
        '''
        with TemporaryDirectory() as tmp_dir:
            constants = WorkspaceConstants(
                workspace_dir=tmp_dir,
                archive_path='/non/existent/examples.tgz'
            )
            service = WorkspaceService(constants=constants)
            self.assertFalse(service.extract_examples())

    def test_extract_examples_success_and_force(self) -> None:
        '''
            Verifies archive unpacking into target directory, both initial and forced.
        '''
        with TemporaryDirectory() as tmp_dir:
            target_ws: str = join(tmp_dir, 'ws')
            constants = WorkspaceConstants(workspace_dir=target_ws)
            service = WorkspaceService(constants=constants)

            self.assertTrue(service.extract_examples(force=False))
            scripts = service.list_scripts()
            self.assertGreater(len(scripts), 0)
            self.assertIn('01_homing.scara', scripts)

            # Test force extraction overwriting existing
            self.assertTrue(service.extract_examples(force=True))

    @patch('scarajectory.infrastructure.storage.workspace.workspace_service.tar_open')
    def test_extract_examples_tar_error(self, mock_tar_open: object) -> None:
        '''
            Verifies error handling on archive decompression fault.
        '''
        mock_tar_open.side_effect = TarError('Corrupt archive')
        with TemporaryDirectory() as tmp_dir:
            constants = WorkspaceConstants(workspace_dir=tmp_dir)
            service = WorkspaceService(constants=constants)
            self.assertFalse(service.extract_examples())

    def test_ensure_workspace_missing_and_existing(self) -> None:
        '''
            Verifies directory creation and conditional examples extraction.
        '''
        with TemporaryDirectory() as tmp_dir:
            target_ws: str = join(tmp_dir, 'new_ws')
            constants = WorkspaceConstants(workspace_dir=target_ws)
            service = WorkspaceService(constants=constants)

            result_dir = service.ensure_workspace()
            self.assertEqual(result_dir, target_ws)
            self.assertTrue(exists(target_ws))
            self.assertGreater(len(service.list_scripts()), 0)

            # Calling again when scripts already present
            again_dir = service.ensure_workspace()
            self.assertEqual(again_dir, target_ws)


if __name__ == '__main__':
    main()
