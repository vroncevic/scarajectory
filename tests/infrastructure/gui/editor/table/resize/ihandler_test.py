# -*- coding: UTF-8 -*-

'''
Module
    ihandler_test.py
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
    Unit tests for ITableResizeHandler interface and protocol conformance.
'''

from __future__ import annotations

from tkinter.ttk import Treeview
from unittest import TestCase, main

from scarajectory.infrastructure.gui.editor.table.resize.ihandler import ITableResizeHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingResizeHandlerStub:
    '''
        Conforming stub implementation satisfying ITableResizeHandler.

        It defines:

            :methods:
                | handle_resize - Simulates table resize handling.
                | get_version - Returns version string.
    '''

    def handle_resize(self, tree: Treeview, event: object) -> None:
        '''
            Simulates table resize handling.

            :param tree: Target Treeview widget.
            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        _ = tree
        _ = event

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'


class IncompleteResizeHandlerStub:
    '''
        Non-conforming stub missing protocol methods.

        It defines:

            :methods:
                | get_version - Returns version string.
                | dummy_method - Dummy test method.
    '''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'

    def dummy_method(self) -> None:
        '''
            Dummy test method.

            :exceptions: None.
        '''


class TestITableResizeHandler(TestCase):
    '''
        Tests verifying ITableResizeHandler protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
                | test_incomplete_stub_failure - Verifies incomplete stub fails protocol check.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on ITableResizeHandler protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(ITableResizeHandler, 'handle_resize'))
        self.assertTrue(hasattr(ITableResizeHandler, 'get_version'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies ITableResizeHandler structurally.

            :exceptions: None.
        '''
        stub = ConformingResizeHandlerStub()
        self.assertIsInstance(stub, ITableResizeHandler)

    def test_incomplete_stub_failure(self) -> None:
        '''
            Verifies incomplete stub fails protocol check.

            :exceptions: None.
        '''
        stub = IncompleteResizeHandlerStub()
        self.assertNotIsInstance(stub, ITableResizeHandler)


if __name__ == '__main__':
    main()
