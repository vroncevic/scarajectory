# -*- coding: UTF-8 -*-

'''
Module
    launcher_test.py
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
    Unit tests for EmulatorLauncher adapter.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.emulator.launcher.ilauncher import IEmulatorLauncher
from scarajectory.infrastructure.gui.emulator.launcher.launcher import EmulatorLauncher
from scarajectory.infrastructure.gui.emulator.locator.ilocator import IEmulatorLocator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EmulatorLauncherTestCase(TestCase):
    '''
        Test suite validating EmulatorLauncher behavior and error handling.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies structural protocol conformance.
                | test_is_available - Verifies availability check logic.
                | test_launch_preview_empty_code - Verifies empty code validation.
                | test_launch_preview_unavailable - Verifies error reporting when locator returns false.
                | test_launch_preview_execution - Verifies successful launch and OSError handling.
                | test_constants_and_version - Verifies ClassVar constants and version string retrieval.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that EmulatorLauncher structurally conforms to IEmulatorLauncher.

            :exceptions: None.
        '''
        mock_locator = MagicMock(spec=IEmulatorLocator)
        launcher = EmulatorLauncher(locator=mock_locator)
        self.assertIsInstance(launcher, IEmulatorLauncher)

    def test_is_available(self) -> None:
        '''
            Verifies availability check delegates to injected locator.

            :exceptions: None.
        '''
        mock_locator = MagicMock(spec=IEmulatorLocator)
        mock_locator.is_available.return_value = True
        launcher = EmulatorLauncher(locator=mock_locator)
        self.assertTrue(launcher.is_available())
        mock_locator.is_available.return_value = False
        self.assertFalse(launcher.is_available())

    def test_launch_preview_empty_code(self) -> None:
        '''
            Verifies that empty code fails immediately without spawning a process.

            :exceptions: None.
        '''
        mock_locator = MagicMock(spec=IEmulatorLocator)
        launcher = EmulatorLauncher(locator=mock_locator)
        success, msg = launcher.launch_preview(dsl_code='   ')
        self.assertFalse(success)
        self.assertEqual(msg, EmulatorLauncher.MSG_EMPTY_CODE)

    def test_launch_preview_unavailable(self) -> None:
        '''
            Verifies error reporting when emulator is not available.

            :exceptions: None.
        '''
        mock_locator = MagicMock(spec=IEmulatorLocator)
        mock_locator.is_available.return_value = False
        launcher = EmulatorLauncher(locator=mock_locator)
        success, msg = launcher.launch_preview(dsl_code='HOME')
        self.assertFalse(success)
        self.assertEqual(msg, EmulatorLauncher.MSG_UNAVAILABLE)

    @patch('scarajectory.infrastructure.gui.emulator.launcher.launcher.spawnve')
    def test_launch_preview_execution(self, mock_spawnve: MagicMock) -> None:
        '''
            Verifies successful launch and handling of OSError during process launch.

            :param mock_spawnve: Mocked os.spawnve function.
            :exceptions: None.
        '''
        mock_locator = MagicMock(spec=IEmulatorLocator)
        mock_locator.is_available.return_value = True
        mock_locator.build_command.return_value = [
            'scaraemu', 'emulator', '--file', '/tmp/test.scara'
        ]
        mock_locator.build_environment.return_value = {}
        launcher = EmulatorLauncher(locator=mock_locator)

        # Success case
        mock_spawnve.return_value = 12345
        success, msg = launcher.launch_preview(dsl_code='MOVE_L X=10.0')
        self.assertTrue(success)
        self.assertIn('Launched', msg)
        mock_spawnve.assert_called_once()

        # OSError case
        mock_spawnve.side_effect = OSError('Permission denied')
        err_success, err_msg = launcher.launch_preview(dsl_code='MOVE_L X=10.0')
        self.assertFalse(err_success)
        self.assertIn('Permission denied', err_msg)

    def test_constants_and_version(self) -> None:
        '''
            Verifies ClassVar constants and version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(EmulatorLauncher.FILE_MODE, 'w')
        self.assertEqual(EmulatorLauncher.FILE_SUFFIX, '.scara')
        self.assertEqual(EmulatorLauncher.FILE_ENCODING, 'utf-8')
        self.assertFalse(EmulatorLauncher.DELETE_ON_CLOSE)
        mock_locator = MagicMock(spec=IEmulatorLocator)
        launcher = EmulatorLauncher(locator=mock_locator)
        ver: str = launcher.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
