# -*- coding: UTF-8 -*-

'''
Module
    manager_test.py
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
    Unit tests for WorkspaceManager component.
'''

from __future__ import annotations

from io import BytesIO
from os import remove
from os.path import exists, expanduser, isdir, join
from shutil import rmtree
from tarfile import DIRTYPE, TarInfo, open as tar_open
from tempfile import NamedTemporaryFile, mkdtemp
from unittest import TestCase, main

from scarajectory.infrastructure.storage.workspace.config import WorkspaceConfig
from scarajectory.infrastructure.storage.workspace.manager import WorkspaceManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWorkspaceManager(TestCase):
    '''
        Test cases verifying WorkspaceManager operations.

        It defines:

            :methods:
                | test_get_workspace_dir - Verifies workspace path expansion.
                | test_list_scripts_missing_dir - Verifies script listing on missing directory.
                | test_list_scripts_not_a_dir - Verifies script listing when target is a file.
                | test_list_scripts_valid - Verifies listing sorted .scara scripts.
                | test_extract_examples_missing_archive - Verifies extraction returns False on missing archive.
                | test_extract_examples_success - Verifies extraction from real archive.
                | test_ensure_workspace_missing - Verifies ensure_workspace handles creation.
                | test_ensure_workspace_existing_empty - Verifies ensure_workspace extracts when empty.
    '''

    def test_get_workspace_dir(self) -> None:
        '''
            Verifies workspace directory expansion.

            :exceptions: None.
        '''
        config = WorkspaceConfig(workspace_dir='~/.test_scarajectory')
        manager = WorkspaceManager(workspace_config=config)
        self.assertEqual(manager.get_workspace_dir(), expanduser('~/.test_scarajectory'))

    def test_list_scripts_missing_dir(self) -> None:
        '''
            Verifies listing scripts in non-existent directory returns empty list.

            :exceptions: None.
        '''
        missing_dir = '/tmp/nonexistent_scara_dir_12345'
        if exists(missing_dir):
            rmtree(missing_dir)
        manager = WorkspaceManager(workspace_config=WorkspaceConfig(workspace_dir=missing_dir))
        self.assertEqual(manager.list_scripts(), [])

    def test_list_scripts_not_a_dir(self) -> None:
        '''
            Verifies listing scripts returns empty list if path is a file.

            :exceptions: None.
        '''
        with NamedTemporaryFile(delete=False) as tmp_file:
            file_path = tmp_file.name
        manager = WorkspaceManager(workspace_config=WorkspaceConfig(workspace_dir=file_path))
        self.assertEqual(manager.list_scripts(), [])

    def test_list_scripts_valid(self) -> None:
        '''
            Verifies listing valid sorted .scara scripts.

            :exceptions: None.
        '''
        tmp_dir = mkdtemp()
        try:
            with open(join(tmp_dir, 'b.scara'), 'w', encoding='utf-8') as f:
                f.write('test')
            with open(join(tmp_dir, 'a.scara'), 'w', encoding='utf-8') as f:
                f.write('test')
            with open(join(tmp_dir, 'c.txt'), 'w', encoding='utf-8') as f:
                f.write('test')

            manager = WorkspaceManager(workspace_config=WorkspaceConfig(workspace_dir=tmp_dir))
            scripts = manager.list_scripts()
            self.assertEqual(scripts, ['a.scara', 'b.scara'])
        finally:
            if exists(tmp_dir):
                rmtree(tmp_dir)

    def test_extract_examples_missing_archive(self) -> None:
        '''
            Verifies extract_examples returns False when archive does not exist.

            :exceptions: None.
        '''
        config = WorkspaceConfig(archive_path='/nonexistent/archive.tgz')
        manager = WorkspaceManager(workspace_config=config)
        self.assertFalse(manager.extract_examples())

        with NamedTemporaryFile(delete=False) as corrupt_file:
            corrupt_path = corrupt_file.name
            corrupt_file.write(b'not a tar content')
        try:
            corrupt_mgr = WorkspaceManager(
                workspace_config=WorkspaceConfig(archive_path=corrupt_path)
            )
            self.assertFalse(corrupt_mgr.extract_examples())
        finally:
            if exists(corrupt_path):
                remove(corrupt_path)

    def test_extract_examples_success(self) -> None:
        '''
            Verifies extract_examples extracts bundle from valid archive.

            :exceptions: None.
        '''
        tmp_dir = mkdtemp()
        try:
            archive_path = join(tmp_dir, 'test_bundle.tar.gz')
            with tar_open(archive_path, 'w:gz') as tar:
                dir_info = TarInfo(name='folder')
                dir_info.type = DIRTYPE
                tar.addfile(dir_info)
                file_data = b'echo hello'
                file_info = TarInfo(name='folder/example.scara')
                file_info.size = len(file_data)
                tar.addfile(file_info, BytesIO(file_data))

            dest_dir = join(tmp_dir, 'dest')
            test_config = WorkspaceConfig(
                workspace_dir=dest_dir, archive_path=archive_path
            )
            manager = WorkspaceManager(workspace_config=test_config)
            result = manager.extract_examples(force=True)
            self.assertTrue(result)
            self.assertTrue(isdir(dest_dir))
        finally:
            if exists(tmp_dir):
                rmtree(tmp_dir)

    def test_ensure_workspace_missing(self) -> None:
        '''
            Verifies ensure_workspace creates directory and calls extraction.

            :exceptions: None.
        '''
        config = WorkspaceConfig()
        if not exists(config.archive_path):
            self.skipTest('Default archive examples.tgz not present')

        tmp_dir = mkdtemp()
        test_dir = join(tmp_dir, 'new_workspace')
        try:
            test_config = WorkspaceConfig(workspace_dir=test_dir)
            manager = WorkspaceManager(workspace_config=test_config)
            res = manager.ensure_workspace()
            self.assertEqual(res, test_dir)
            self.assertTrue(exists(test_dir))
        finally:
            if exists(tmp_dir):
                rmtree(tmp_dir)

    def test_ensure_workspace_existing_empty(self) -> None:
        '''
            Verifies ensure_workspace extracts when directory is empty.

            :exceptions: None.
        '''
        config = WorkspaceConfig()
        if not exists(config.archive_path):
            self.skipTest('Default archive examples.tgz not present')

        tmp_dir = mkdtemp()
        try:
            test_config = WorkspaceConfig(workspace_dir=tmp_dir)
            manager = WorkspaceManager(workspace_config=test_config)
            res = manager.ensure_workspace()
            self.assertEqual(res, tmp_dir)
        finally:
            if exists(tmp_dir):
                rmtree(tmp_dir)


if __name__ == '__main__':
    main()
