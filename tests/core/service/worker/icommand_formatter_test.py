# -*- coding: UTF-8 -*-

'''
Module
    icommand_formatter_test.py
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
    Unit testing for ICommandFormatter protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.worker.icommand_formatter import ICommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommandFormatterStub:
    '''Structural test stub satisfying ICommandFormatter protocol.'''

    def format_move(self, pt: Waypoint) -> str:
        '''Formats waypoint motion command.'''
        return f'G1 X{pt.x} Y{pt.y}'

    def format_home(self) -> str:
        '''Formats homing command.'''
        return 'G28'


class IncompleteCommandFormatterStub:
    '''Incomplete test stub missing required format_move method.'''

    def format_home(self) -> str:
        '''Formats homing command.'''
        return 'G28'

    def format_estop(self) -> str:
        '''Formats emergency stop command.'''
        return 'M112'


class CommandFormatterTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for ICommandFormatter.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies ICommandFormatter protocol.'''
        stub = CommandFormatterStub()
        self.assertIsInstance(stub, ICommandFormatter)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails ICommandFormatter protocol check.'''
        incomplete = IncompleteCommandFormatterStub()
        self.assertNotIsInstance(incomplete, ICommandFormatter)


if __name__ == '__main__':
    main()
