# -*- coding: UTF-8 -*-

'''
Module
    imenu_bar_test.py
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
    Unit testing for IAppMenuBar protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.menu.imenu_bar import IAppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingMenuBarStub:
    '''Conforming stub implementation satisfying IAppMenuBar.'''

    def open_json_dialog(self) -> None:
        '''Opens JSON dialog.'''

    def save_json_dialog(self) -> None:
        '''Saves JSON dialog.'''

    def import_dsl_dialog(self) -> None:
        '''Imports DSL dialog.'''

    def export_dsl_dialog(self) -> None:
        '''Exports DSL dialog.'''


class IncompleteMenuBarStub:
    '''Non-conforming stub missing export_dsl_dialog.'''

    def open_json_dialog(self) -> None:
        '''Opens JSON dialog.'''

    def save_json_dialog(self) -> None:
        '''Saves JSON dialog.'''

    def import_dsl_dialog(self) -> None:
        '''Imports DSL dialog.'''


class MenuBarProtocolTestCase(TestCase):
    '''
        Tests IAppMenuBar runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies IAppMenuBar protocol.

            :exceptions: None.
        '''
        stub = ConformingMenuBarStub()
        self.assertIsInstance(stub, IAppMenuBar)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-compliant class fails IAppMenuBar protocol check.

            :exceptions: None.
        '''
        stub = IncompleteMenuBarStub()
        self.assertNotIsInstance(stub, IAppMenuBar)


if __name__ == '__main__':
    main()
