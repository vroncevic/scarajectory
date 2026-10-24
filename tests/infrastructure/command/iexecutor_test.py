# -*- coding: UTF-8 -*-

'''
Module
    iexecutor_test.py
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
    Unit testing for ICommandExecutor protocol.
'''

from __future__ import annotations

from collections.abc import Mapping
from unittest import TestCase, main

from scarajectory.infrastructure.command.idefinition import ICommandDefinition
from scarajectory.infrastructure.command.iexecutor import ICommandExecutor

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandExecutorStub:
    '''Structural test stub satisfying ICommandExecutor.'''

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: object,
    ) -> Mapping[str, object]:
        '''Executes command stub.'''
        _ = (params, service)
        return {'returncode': 0}

    def get_definition(self) -> ICommandDefinition:
        '''Gets definition stub.'''
        return None  # type: ignore[return-value]


class IncompleteExecutorStub:
    '''Incomplete stub missing get_definition.'''

    def execute(
        self,
        *,
        params: Mapping[str, object],
        service: object,
    ) -> Mapping[str, object]:
        '''Executes command stub.'''
        _ = (params, service)
        return {'returncode': 0}

    def reset(self) -> None:
        '''Resets stub.'''


class CommandExecutorProtocolTestCase(TestCase):
    '''
        Unit tests for ICommandExecutor protocol runtime check.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies structural compliance.
                | test_protocol_conformance_failure - Verifies incomplete class rejection.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies ICommandExecutor protocol.

            :exceptions: None.
        '''
        stub = CommandExecutorStub()
        self.assertIsInstance(stub, ICommandExecutor)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies incomplete class fails ICommandExecutor protocol check.

            :exceptions: None.
        '''
        incomplete = IncompleteExecutorStub()
        self.assertNotIsInstance(incomplete, ICommandExecutor)


if __name__ == '__main__':
    main()
