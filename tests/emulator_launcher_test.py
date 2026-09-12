# -*- coding: UTF-8 -*-

'''
Module
    emulator_launcher_test.py
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
    Unit tests for EmulatorLauncher adapter and IEmulatorLauncher protocol conformance.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

pkg_dir: str = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.infrastructure.gui.dsl.emulator_launcher import (
    EmulatorLauncher,
)
from scarajectory.infrastructure.gui.dsl.iemulator_launcher import (
    IEmulatorLauncher,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestEmulatorLauncher(TestCase):
    '''
        Test suite validating EmulatorLauncher behavior and error handling.
    '''

    def setUp(self) -> None:
        '''
            Prepares launcher instance for testing.
        '''
        self._launcher = EmulatorLauncher()

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that EmulatorLauncher structurally conforms to IEmulatorLauncher.
        '''
        self.assertTrue(isinstance(self._launcher, IEmulatorLauncher))

    def test_launch_preview_empty_code(self) -> None:
        '''
            Verifies that empty code fails immediately without spawning a process.
        '''
        success, msg = self._launcher.launch_preview(dsl_code='   ')
        self.assertFalse(success)
        self.assertIn('empty', msg.lower())

    @patch('scarajectory.infrastructure.gui.dsl.emulator_launcher.Path.is_file')
    def test_launch_preview_dir_not_found(
        self, mock_is_file: MagicMock
    ) -> None:
        '''
            Verifies error reporting when SCARAEmu directory is not found.
        '''
        mock_is_file.return_value = False
        success, msg = self._launcher.launch_preview(dsl_code='HOME')
        self.assertFalse(success)
        self.assertIn('not found', msg.lower())

    @patch('scarajectory.infrastructure.gui.dsl.emulator_launcher.Popen')
    @patch('scarajectory.infrastructure.gui.dsl.emulator_launcher.Path.is_file')
    def test_launch_preview_success(
        self, mock_is_file: MagicMock, mock_popen: MagicMock
    ) -> None:
        '''
            Verifies successful launch and command line construction.
        '''
        mock_is_file.return_value = True
        success, msg = self._launcher.launch_preview(dsl_code='MOVE_L X=10.0')
        self.assertTrue(success)
        self.assertIn('Launched', msg)
        mock_popen.assert_called_once()

    @patch('scarajectory.infrastructure.gui.dsl.emulator_launcher.Popen')
    @patch('scarajectory.infrastructure.gui.dsl.emulator_launcher.Path.is_file')
    def test_launch_preview_os_error(
        self, mock_is_file: MagicMock, mock_popen: MagicMock
    ) -> None:
        '''
            Verifies handling of OSError during process launch.
        '''
        mock_is_file.return_value = True
        mock_popen.side_effect = OSError('Permission denied')
        success, msg = self._launcher.launch_preview(dsl_code='MOVE_L X=10.0')
        self.assertFalse(success)
        self.assertIn('Permission denied', msg)


if __name__ == '__main__':
    main()
