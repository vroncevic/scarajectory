# -*- coding: UTF-8 -*-

'''
Module
    iassembler_test.py
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
    Unit tests for ISectionsAssembler protocol conformance.
'''

from __future__ import annotations

from tkinter import Widget
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle
from scarajectory.infrastructure.gui.toolbar.section.iassembler import ISectionsAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingSectionsAssemblerStub:
    '''Conforming stub implementation satisfying ISectionsAssembler protocol.'''

    def assemble_sections(
        self,
        parent: Widget,
        bundle: ToolbarBundle,
    ) -> SectionsBundle:
        '''
            Assembles sections into SectionsBundle.

            :param parent: Parent container widget.
            :param bundle: Toolbar bundle.
            :return: Sections bundle.
            :exceptions: None.
        '''
        _ = (parent, bundle)
        return MagicMock(spec=SectionsBundle)

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.3'


class IncompleteSectionsAssemblerStub:
    '''Non-conforming stub implementation missing assemble_sections.'''

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.3'

    def is_active(self) -> bool:
        '''
            Checks active status.

            :return: False.
            :exceptions: None.
        '''
        return False


class ISectionsAssemblerTestCase(TestCase):
    '''
        Tests ISectionsAssembler runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_protocol_methods - Verifies protocol defines required methods.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''
            Verifies compliant class satisfies ISectionsAssembler protocol.

            :exceptions: None.
        '''
        stub = ConformingSectionsAssemblerStub()
        self.assertIsInstance(stub, ISectionsAssembler)

    def test_protocol_conformance_failure(self) -> None:
        '''
            Verifies non-compliant class fails ISectionsAssembler protocol check.

            :exceptions: None.
        '''
        stub = IncompleteSectionsAssemblerStub()
        self.assertNotIsInstance(stub, ISectionsAssembler)

    def test_protocol_methods(self) -> None:
        '''
            Verifies protocol defines expected method attributes.

            :exceptions: None.
        '''
        for method_name in ('assemble_sections', 'get_version'):
            self.assertTrue(hasattr(ISectionsAssembler, method_name))


if __name__ == '__main__':
    main()
