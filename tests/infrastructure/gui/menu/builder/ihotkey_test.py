# -*- coding: UTF-8 -*-

'''
Module
    ihotkey_test.py
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
    Unit testing for IMenuHotkeyBinder protocol conformance.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main

from scarajectory.infrastructure.gui.menu.builder.ihotkey import IMenuHotkeyBinder
from scarajectory.infrastructure.gui.menu.bundle import MenuBundle
from scarajectory.infrastructure.gui.menu.imenu_bar import IAppMenuBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingHotkeyBinderStub:
    '''Conforming stub implementation satisfying IMenuHotkeyBinder.'''

    def bind_hotkeys(
        self,
        root: Tk,
        menu_bar: IAppMenuBar,
        bundle: MenuBundle,
    ) -> None:
        '''Binds keyboard shortcuts.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'


class IncompleteHotkeyBinderStub:
    '''Non-conforming stub missing bind_hotkeys.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.0'

    def dummy_action(self) -> None:
        '''Dummy method for public method threshold.'''


class MenuHotkeyBinderProtocolTestCase(TestCase):
    '''
        Tests IMenuHotkeyBinder runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies IMenuHotkeyBinder protocol.

            :exceptions: None.
        '''
        stub = ConformingHotkeyBinderStub()
        self.assertIsInstance(stub, IMenuHotkeyBinder)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-compliant class fails IMenuHotkeyBinder protocol check.

            :exceptions: None.
        '''
        stub = IncompleteHotkeyBinderStub()
        self.assertNotIsInstance(stub, IMenuHotkeyBinder)


if __name__ == '__main__':
    main()
