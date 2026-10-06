# -*- coding: UTF-8 -*-

'''
Module
    itable_test.py
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
    Unit testing for ITable protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.table.itable import ITable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingTableStub:
    '''Conforming stub implementation satisfying ITable.'''

    def refresh_table(self) -> None:
        '''Refreshes table rows.'''

    def delete_selected(self) -> None:
        '''Deletes selected item.'''


class IncompleteTableStub:
    '''Non-conforming stub implementation missing delete_selected.'''

    def refresh_table(self) -> None:
        '''Refreshes table rows.'''

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class TableProtocolTestCase(TestCase):
    '''
        Tests ITable runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies ITable protocol.'''
        stub = ConformingTableStub()
        self.assertIsInstance(stub, ITable)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails ITable protocol check.'''
        stub = IncompleteTableStub()
        self.assertNotIsInstance(stub, ITable)


if __name__ == '__main__':
    main()
