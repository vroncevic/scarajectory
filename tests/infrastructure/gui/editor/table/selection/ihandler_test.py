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
    Unit tests for ITableSelectionHandler interface and protocol conformance.
'''

from __future__ import annotations

from tkinter.ttk import Treeview
from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.selection.coordinator.icoordinator import IPlanSelectionCoordinator
from scarajectory.infrastructure.gui.editor.table.selection.ihandler import ITableSelectionHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingSelectionHandlerStub:
    '''
        Conforming stub implementation satisfying ITableSelectionHandler.

        It defines:

            :methods:
                | handle_selection - Simulates table row selection handling.
                | get_version - Returns version string.
    '''

    def handle_selection(
        self, tree: Treeview, selection: IPlanSelectionCoordinator
    ) -> None:
        '''
            Simulates table row selection handling.

            :param tree: Target Treeview widget.
            :param selection: Injected IPlanSelectionCoordinator instance.
            :exceptions: None.
        '''
        _ = tree
        _ = selection

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.0'


class IncompleteSelectionHandlerStub:
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


class TestITableSelectionHandler(TestCase):
    '''
        Tests verifying ITableSelectionHandler protocol definition and subtyping.

        It defines:

            :methods:
                | test_protocol_methods - Verifies methods declared on protocol.
                | test_conforming_stub_subtyping - Verifies stub satisfies protocol.
                | test_incomplete_stub_failure - Verifies incomplete stub fails protocol check.
    '''

    def test_protocol_methods(self) -> None:
        '''
            Verifies methods declared on ITableSelectionHandler protocol.

            :exceptions: None.
        '''
        self.assertTrue(hasattr(ITableSelectionHandler, 'handle_selection'))
        self.assertTrue(hasattr(ITableSelectionHandler, 'get_version'))

    def test_conforming_stub_subtyping(self) -> None:
        '''
            Verifies conforming stub satisfies ITableSelectionHandler structurally.

            :exceptions: None.
        '''
        stub = ConformingSelectionHandlerStub()
        self.assertIsInstance(stub, ITableSelectionHandler)

    def test_incomplete_stub_failure(self) -> None:
        '''
            Verifies incomplete stub fails protocol check.

            :exceptions: None.
        '''
        stub = IncompleteSelectionHandlerStub()
        self.assertNotIsInstance(stub, ITableSelectionHandler)


if __name__ == '__main__':
    main()
