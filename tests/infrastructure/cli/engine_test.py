# -*- coding: UTF-8 -*-

'''
Module
    engine_test.py
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
    Unit testing for CLI adapter engine.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.exceptions import ATSRuntimeError, ATSValueError
from ats_utilities.option.imanager import IOptionManager

from scarajectory.core.service.iservice import IService
from scarajectory.infrastructure.cli.engine import CLI
from scarajectory.infrastructure.cli.setup.bundle import CLIBundle
from scarajectory.infrastructure.command.command_bundle import CommandBundle
from scarajectory.infrastructure.command.icommand_definition import ICommandDefinition
from scarajectory.infrastructure.command.icommand_executor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CLITestCase(TestCase):
    '''
        Unit tests for CLI command dispatcher adapter.

        It defines:

            :methods:
                | setUp - Initializes mock service, parser, and executor bundle.
                | test_initialization_and_str - Verifies initialization flag and string format.
                | test_run_success - Verifies successful command dispatch and return values.
                | test_run_command_not_found - Verifies error result when command is unregistered.
                | test_run_exceptions - Verifies error recovery when parser raises exceptions.
    '''

    def setUp(self) -> None:
        '''Initializes mock CLI collaborators before each test.'''
        self.mock_service = MagicMock(spec=IService)
        self.mock_parser = MagicMock(spec=IOptionManager)
        self.mock_definition = MagicMock(spec=ICommandDefinition)
        self.mock_definition.name = 'test_cmd'
        self.mock_executor = MagicMock(spec=ICommandExecutor)

        cmd_bundle = CommandBundle(
            definition=self.mock_definition,
            executor=self.mock_executor,
        )
        self.bundle = CLIBundle(
            service=self.mock_service,
            parser=self.mock_parser,
            commands=[cmd_bundle],
        )

    def test_initialization_and_str(self) -> None:
        '''Verifies initialization state, command registration, and string output.'''
        cli = CLI(self.bundle)
        self.assertTrue(cli.is_initialized())
        self.assertIsInstance(str(cli), str)
        self.mock_parser.register_commands.assert_called_once_with(
            [self.mock_definition]
        )

    def test_run_success(self) -> None:
        '''Verifies execution of matched command strategy and returned result mapping.'''
        cli = CLI(self.bundle)
        self.mock_parser.parse_command.return_value = (
            'test_cmd', {'target': 'studio'}
        )
        expected = {'returncode': 0, 'stdout': 'Done', 'stderr': ''}
        self.mock_executor.execute.return_value = expected

        result = cli.run()
        self.assertEqual(result, expected)
        self.mock_executor.execute.assert_called_once_with(
            params={'target': 'studio'}, service=self.mock_service
        )

    def test_run_command_not_found(self) -> None:
        '''Verifies error mapping when parser outputs unknown command name.'''
        cli = CLI(self.bundle)
        self.mock_parser.parse_command.return_value = (
            'unknown_cmd', {}
        )
        result = cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('command not found', str(result['stderr']))

    def test_run_exceptions(self) -> None:
        '''Verifies catching ATS exceptions during argument parsing.'''
        cli = CLI(self.bundle)
        self.mock_parser.parse_command.side_effect = ATSValueError(
            'Missing option'
        )
        result = cli.run()
        self.assertEqual(result['returncode'], 1)
        self.assertIn('Missing option', str(result['stderr']))

        self.mock_parser.parse_command.side_effect = ATSRuntimeError(
            'Parsing error'
        )
        result_runtime = cli.run()
        self.assertEqual(result_runtime['returncode'], 1)
        self.assertIn('Parsing error', str(result_runtime['stderr']))


if __name__ == '__main__':
    main()
