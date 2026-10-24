# -*- coding: UTF-8 -*-

'''
Module
    idefinition_test.py
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
    Unit testing for ICommandDefinition protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from ats_utilities.option.command.data import OptionData

from scarajectory.infrastructure.command.idefinition import ICommandDefinition

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandDefinitionStub:
    '''Structural test stub satisfying ICommandDefinition.'''

    @property
    def name(self) -> str:
        '''Returns name.'''
        return 'test'

    @property
    def help_text(self) -> str:
        '''Returns help text.'''
        return 'test help'

    @property
    def options(self) -> Sequence[OptionData]:
        '''Returns options.'''
        return ()

    def get_version(self) -> str:
        '''Returns version.'''
        return '1.0.0'


class IncompleteDefinitionStub:
    '''Incomplete stub missing get_version.'''

    @property
    def name(self) -> str:
        '''Returns name.'''
        return 'incomplete'

    @property
    def help_text(self) -> str:
        '''Returns help text.'''
        return 'incomplete'


class CommandDefinitionProtocolTestCase(TestCase):
    '''
        Unit tests for ICommandDefinition protocol runtime check.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies structural compliance.
                | test_protocol_conformance_failure - Verifies incomplete class rejection.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies ICommandDefinition protocol.

            :exceptions: None.
        '''
        stub = CommandDefinitionStub()
        self.assertIsInstance(stub, ICommandDefinition)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies incomplete class fails ICommandDefinition protocol check.

            :exceptions: None.
        '''
        incomplete = IncompleteDefinitionStub()
        self.assertNotIsInstance(incomplete, ICommandDefinition)


if __name__ == '__main__':
    main()
