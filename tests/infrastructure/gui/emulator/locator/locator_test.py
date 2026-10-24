# -*- coding: UTF-8 -*-

'''
Module
    locator_test.py
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
    Unit testing for EmulatorLocator component.
'''

from __future__ import annotations

from json import dumps as json_dumps
from tempfile import NamedTemporaryFile
from unittest import TestCase, main
from unittest.mock import patch

from scarajectory.infrastructure.gui.emulator.locator.ilocator import IEmulatorLocator
from scarajectory.infrastructure.gui.emulator.locator.locator import EmulatorLocator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorLocatorTestCase(TestCase):
    '''
        Unit tests for EmulatorLocator discovery, resolution, and command generation.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies EmulatorLocator conforms to IEmulatorLocator.
                | test_resolve_target_from_environment - Verifies resolution via SCARAEMU_PATH.
                | test_resolve_target_from_config - Verifies resolution via scaraemu.json configuration.
                | test_resolve_target_from_which - Verifies resolution via system PATH.
                | test_build_command_and_environment - Verifies command list and environment construction.
                | test_constants_and_version - Verifies ClassVar constants and version retrieval.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies EmulatorLocator satisfies IEmulatorLocator structurally.

            :exceptions: None.
        '''
        locator = EmulatorLocator(config_path='/tmp/nonexistent.json')
        self.assertIsInstance(locator, IEmulatorLocator)

    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.isdir')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.isfile')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.environ', {'SCARAEMU_PATH': '/opt/custom/main.py'})
    def test_resolve_target_from_environment(self, mock_isfile, mock_isdir) -> None:
        '''
            Verifies resolution via SCARAEMU_PATH environment variable.

            :param mock_isfile: Mocked os.path.isfile.
            :param mock_isdir: Mocked os.path.isdir.
            :exceptions: None.
        '''
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        locator = EmulatorLocator(config_path='/tmp/nonexistent.json')
        target_type, target_path = locator.resolve_target()
        self.assertEqual(target_type, EmulatorLocator.TARGET_SCRIPT)
        self.assertEqual(target_path, '/opt/custom/main.py')
        self.assertTrue(locator.is_available())

        mock_isdir.return_value = True
        with patch('scarajectory.infrastructure.gui.emulator.locator.locator.environ', {'SCARAEMU_PATH': '/opt/custom_dir'}):
            target_type, target_path = locator.resolve_target()
            self.assertEqual(target_type, EmulatorLocator.TARGET_SCRIPT)
            self.assertEqual(target_path, '/opt/custom_dir/main.py')

        mock_isdir.return_value = False
        with patch('scarajectory.infrastructure.gui.emulator.locator.locator.environ', {'SCARAEMU_PATH': '/opt/custom_bin'}):
            target_type, target_path = locator.resolve_target()
            self.assertEqual(target_type, EmulatorLocator.TARGET_BINARY)
            self.assertEqual(target_path, '/opt/custom_bin')

    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.isdir')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.isfile')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.environ', {})
    def test_resolve_target_from_config(self, mock_isfile, mock_isdir) -> None:
        '''
            Verifies resolution via scaraemu.json configuration file.

            :param mock_isfile: Mocked os.path.isfile.
            :param mock_isdir: Mocked os.path.isdir.
            :exceptions: None.
        '''
        mock_isdir.return_value = False
        mock_isfile.return_value = True
        payload: str = json_dumps({
            'tool_path': '/usr/local/bin/scaraemu_custom',
            'main_module': 'main.py',
        })
        with NamedTemporaryFile(mode='w', suffix='.json', delete=True, encoding='utf-8') as tmp:
            tmp.write(payload)
            tmp.flush()
            locator = EmulatorLocator(config_path=tmp.name)
            target_type, target_path = locator.resolve_target()
            self.assertEqual(target_type, EmulatorLocator.TARGET_BINARY)
            self.assertEqual(target_path, '/usr/local/bin/scaraemu_custom')

        mock_isdir.return_value = True
        dir_payload: str = json_dumps({
            'tool_path': '/opt/custom_pkg',
            'main_module': 'main.py',
        })
        with NamedTemporaryFile(mode='w', suffix='.json', delete=True, encoding='utf-8') as tmp:
            tmp.write(dir_payload)
            tmp.flush()
            locator = EmulatorLocator(config_path=tmp.name)
            target_type, target_path = locator.resolve_target()
            self.assertEqual(target_type, EmulatorLocator.TARGET_SCRIPT)
            self.assertEqual(target_path, '/opt/custom_pkg/main.py')

        mock_isdir.return_value = False
        script_payload: str = json_dumps({
            'tool_path': '/opt/custom_pkg/custom.py',
        })
        with NamedTemporaryFile(mode='w', suffix='.json', delete=True, encoding='utf-8') as tmp:
            tmp.write(script_payload)
            tmp.flush()
            locator = EmulatorLocator(config_path=tmp.name)
            target_type, target_path = locator.resolve_target()
            self.assertEqual(target_type, EmulatorLocator.TARGET_SCRIPT)
            self.assertEqual(target_path, '/opt/custom_pkg/custom.py')

    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.isfile')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.which')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.exists')
    @patch('scarajectory.infrastructure.gui.emulator.locator.locator.environ', {})
    def test_resolve_target_from_which(self, mock_exists, mock_which, mock_isfile) -> None:
        '''
            Verifies resolution via system which utility on PATH.

            :param mock_exists: Mocked os.path.exists.
            :param mock_which: Mocked shutil.which.
            :param mock_isfile: Mocked os.path.isfile.
            :exceptions: None.
        '''
        mock_exists.return_value = False
        mock_which.return_value = '/usr/bin/scaraemu'
        locator = EmulatorLocator(config_path='/tmp/nonexistent.json')
        target_type, target_path = locator.resolve_target()
        self.assertEqual(target_type, EmulatorLocator.TARGET_BINARY)
        self.assertEqual(target_path, '/usr/bin/scaraemu')

        mock_which.return_value = None
        mock_isfile.return_value = True
        target_type, target_path = locator.resolve_target()
        self.assertEqual(target_type, EmulatorLocator.TARGET_SCRIPT)
        self.assertTrue(target_path.endswith('main.py'))

        mock_isfile.return_value = False
        target_type, target_path = locator.resolve_target()
        self.assertEqual(target_type, EmulatorLocator.TARGET_NONE)
        self.assertEqual(target_path, '')
        self.assertFalse(locator.is_available())

    @patch.object(EmulatorLocator, 'resolve_target')
    def test_build_command_and_environment(self, mock_resolve) -> None:
        '''
            Verifies build_command and build_environment construction.

            :param mock_resolve: Mocked resolve_target method.
            :exceptions: None.
        '''
        mock_resolve.return_value = (EmulatorLocator.TARGET_SCRIPT, '/home/user/scaraemu/main.py')
        locator = EmulatorLocator(config_path='/tmp/nonexistent.json')
        cmd = locator.build_command(file_path='/tmp/test.scara')
        self.assertIn('emulator', cmd)
        self.assertIn('--file', cmd)
        self.assertIn('/tmp/test.scara', cmd)

        with patch.dict('scarajectory.infrastructure.gui.emulator.locator.locator.environ', {'PYTHONPATH': '/existing'}, clear=False):
            env = locator.build_environment()
            self.assertIn('PYTHONPATH', env)
            self.assertTrue(env['PYTHONPATH'].startswith('/home/user/scaraemu:/existing'))

        mock_resolve.return_value = (EmulatorLocator.TARGET_BINARY, '/usr/bin/scaraemu')
        cmd_bin = locator.build_command(file_path='/tmp/test.scara')
        self.assertEqual(cmd_bin[0], '/usr/bin/scaraemu')

        mock_resolve.return_value = (EmulatorLocator.TARGET_NONE, '')
        cmd_none = locator.build_command(file_path='/tmp/test.scara')
        self.assertEqual(cmd_none, [])
        env_none = locator.build_environment()
        self.assertIsInstance(env_none, dict)


    def test_constants_and_version(self) -> None:
        '''
            Verifies ClassVar constants and version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(EmulatorLocator.TARGET_BINARY, 'binary')
        self.assertEqual(EmulatorLocator.TARGET_SCRIPT, 'script')
        self.assertEqual(EmulatorLocator.TARGET_NONE, 'none')
        self.assertEqual(EmulatorLocator.ENV_TOOL_PATH, 'SCARAEMU_PATH')
        self.assertEqual(EmulatorLocator.ENV_MAIN_MODULE, 'SCARAEMU_MAIN')
        self.assertEqual(EmulatorLocator.EXECUTABLE_NAME, 'scaraemu')
        self.assertEqual(EmulatorLocator.COMMAND_EMULATOR, 'emulator')
        self.assertEqual(EmulatorLocator.OPTION_FILE, '--file')
        locator = EmulatorLocator(config_path='/tmp/nonexistent.json')
        ver = locator.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
