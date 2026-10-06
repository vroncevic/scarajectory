# -*- coding: UTF-8 -*-

'''
Module
    itabs_assembler_test.py
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
    Unit tests for ITabsAssembler protocol conformance.
'''

from __future__ import annotations

from tkinter.ttk import Notebook
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.itabs_assembler import ITabsAssembler
from scarajectory.infrastructure.gui.controls.tabs_bundle import ControlsTabsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingTabsAssemblerStub:
    '''Conforming stub implementation satisfying ITabsAssembler protocol.'''

    def assemble_tabs(
        self,
        notebook: Notebook,
        bundle: ControlsBundle,
    ) -> ControlsTabsBundle:
        '''Assembles tabs into ControlsTabsBundle.'''
        _ = (notebook, bundle)
        return MagicMock(spec=ControlsTabsBundle)

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.3'


class IncompleteTabsAssemblerStub:
    '''Non-conforming stub implementation missing assemble_tabs.'''

    def get_version(self) -> str:
        '''Returns version string.'''
        return '1.0.3'

    def is_active(self) -> bool:
        '''Checks active status.'''
        return False


class ITabsAssemblerTestCase(TestCase):
    '''
        Tests ITabsAssembler runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_protocol_methods - Verifies protocol defines required methods.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies ITabsAssembler protocol.'''
        stub = ConformingTabsAssemblerStub()
        self.assertIsInstance(stub, ITabsAssembler)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails ITabsAssembler protocol check.'''
        stub = IncompleteTabsAssemblerStub()
        self.assertNotIsInstance(stub, ITabsAssembler)

    def test_protocol_methods(self) -> None:
        '''Verifies protocol defines expected method attributes.'''
        for method_name in ('assemble_tabs', 'get_version'):
            self.assertTrue(hasattr(ITabsAssembler, method_name))


if __name__ == '__main__':
    main()
