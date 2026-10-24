# -*- coding: UTF-8 -*-

'''
Module
    executor_test.py
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
    Unit testing for StudioCommandExecutor.
'''

from __future__ import annotations

from collections.abc import Mapping
from unittest import TestCase, main

from scarajectory.infrastructure.command.studio.definition import StudioCommandDefinition
from scarajectory.infrastructure.command.studio.executor import StudioCommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubGUI:
    '''Structural stub for GUI presentation adapter.'''

    def __init__(self, initialized: bool = True, raise_on_start: bool = False) -> None:
        self.initialized: bool = initialized
        self.raise_on_start: bool = raise_on_start
        self.loaded_file: str = ''
        self.deadzone_enabled: bool = False
        self.started: bool = False
        self.stopped: bool = False

    def is_initialized(self) -> bool:
        '''Checks initialization state.'''
        return self.initialized

    def load_file(self, file_path: str) -> bool:
        '''Simulates loading a trajectory plan file.'''
        self.loaded_file = file_path
        return True

    def set_deadzone(self, enabled: bool) -> None:
        '''Sets dead zone enforcement.'''
        self.deadzone_enabled = enabled

    def start(self) -> None:
        '''Simulates starting the GUI main loop.'''
        if self.raise_on_start:
            raise RuntimeError('Failed to start GUI')
        self.started = True

    def stop(self) -> None:
        '''Simulates closing the GUI.'''
        self.stopped = True


class StudioCommandExecutorTestCase(TestCase):
    '''
        Test cases verifying StudioCommandExecutor.

        It defines:

            :methods:
                | test_execute_uninitialized_gui - Verifies error when GUI is not initialized.
                | test_execute_with_none_service - Verifies command execution when service is None.
                | test_execute_success - Verifies full execution path with file and deadzone params.
                | test_execute_failure_on_exception - Verifies safe error handling on GUI crash.
                | test_get_definition_and_string - Verifies definition accessor and string cast.
    '''

    def test_execute_uninitialized_gui(self) -> None:
        '''
            Verifies command failure when GUI is uninitialized.

            :exceptions: None.
        '''
        definition = StudioCommandDefinition()
        gui = StubGUI(initialized=False)
        executor = StudioCommandExecutor(definition=definition, gui=gui)

        result: Mapping[str, object] = executor.execute(params={}, service=None)
        self.assertEqual(result['returncode'], 1)
        self.assertIn('gui not initialized', str(result['stderr']))

    def test_execute_with_none_service(self) -> None:
        '''
            Verifies command execution when service is None.

            :exceptions: None.
        '''
        definition = StudioCommandDefinition()
        gui = StubGUI(initialized=True)
        executor = StudioCommandExecutor(definition=definition, gui=gui)

        result: Mapping[str, object] = executor.execute(params={}, service=None)
        self.assertEqual(result['returncode'], 0)
        self.assertTrue(gui.started)

    def test_execute_success(self) -> None:
        '''
            Verifies successful command execution passing file and deadzone parameters.

            :exceptions: None.
        '''
        definition = StudioCommandDefinition()
        gui = StubGUI(initialized=True)
        executor = StudioCommandExecutor(definition=definition, gui=gui)

        params: dict[str, object] = {
            'file': '/tmp/test_plan.json',
            'dead_zone': True,
        }
        result: Mapping[str, object] = executor.execute(params=params, service=None)
        self.assertEqual(result['returncode'], 0)
        self.assertEqual(gui.loaded_file, '/tmp/test_plan.json')
        self.assertTrue(gui.deadzone_enabled)
        self.assertTrue(gui.started)

    def test_execute_failure_on_exception(self) -> None:
        '''
            Verifies graceful exception handling when GUI start raises an exception.

            :exceptions: None.
        '''
        definition = StudioCommandDefinition()
        gui = StubGUI(initialized=True, raise_on_start=True)
        executor = StudioCommandExecutor(definition=definition, gui=gui)

        result: Mapping[str, object] = executor.execute(params={}, service=None)
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Failed to start GUI', str(result['stderr']))

    def test_get_definition_and_string(self) -> None:
        '''
            Verifies get_definition and string representation of executor.

            :exceptions: None.
        '''
        definition = StudioCommandDefinition()
        gui = StubGUI(initialized=True)
        executor = StudioCommandExecutor(definition=definition, gui=gui)
        self.assertIs(executor.get_definition(), definition)
        self.assertIn('StudioCommandExecutor', str(executor))


if __name__ == '__main__':
    main()
