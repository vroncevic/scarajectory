# -*- coding: UTF-8 -*-

'''
Module
    assembler_test.py
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
    Unit tests for SectionsAssembler toolbar section assembly service.
'''

from __future__ import annotations

from tkinter import Widget
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.section.assembler import SectionsAssembler
from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle
from scarajectory.infrastructure.gui.toolbar.section.navigation import NavigationSection
from scarajectory.infrastructure.gui.toolbar.section.parameter import ParameterSection
from scarajectory.infrastructure.gui.toolbar.section.status import StatusSection
from scarajectory.infrastructure.gui.toolbar.section.tool import ToolSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SectionsAssemblerTestCase(TestCase):
    '''
        Tests SectionsAssembler section construction operations.

        It defines:

            :methods:
                | test_assembler_version - Verifies version string getter.
                | test_assemble_sections - Verifies instantiation and packing of toolbar sections.
    '''

    def test_assembler_version(self) -> None:
        '''
            Verifies version string reported by assembler.

            :exceptions: None.
        '''
        assembler = SectionsAssembler()
        self.assertEqual(assembler.get_version(), '1.0.3')

    def test_assemble_sections(self) -> None:
        '''
            Verifies all sections are assembled and bundled correctly.

            :exceptions: None.
        '''
        target_pkg = 'scarajectory.infrastructure.gui.toolbar.section.assembler.'
        with (
            patch(f'{target_pkg}ToolSection') as mock_tool_cls,
            patch(f'{target_pkg}NavigationSection') as mock_nav_cls,
            patch(f'{target_pkg}ParameterSection') as mock_param_cls,
            patch(f'{target_pkg}StatusSection') as mock_status_cls,
            patch(f'{target_pkg}Separator') as mock_sep_cls,
        ):
            mock_tool_inst = MagicMock(spec=ToolSection)
            mock_nav_inst = MagicMock(spec=NavigationSection)
            mock_param_inst = MagicMock(spec=ParameterSection)
            mock_status_inst = MagicMock(spec=StatusSection)

            mock_tool_cls.return_value = mock_tool_inst
            mock_nav_cls.return_value = mock_nav_inst
            mock_param_cls.return_value = mock_param_inst
            mock_status_cls.return_value = mock_status_inst

            mock_parent = MagicMock(spec=Widget)
            mock_bundle = MagicMock(spec=ToolbarBundle)
            mock_bundle.r_min = 100.0
            mock_bundle.r_max = 500.0

            result = SectionsAssembler().assemble_sections(
                mock_parent, mock_bundle
            )

            self.assertIsInstance(result, SectionsBundle)
            self.assertIs(result.tool_section, mock_tool_inst)
            self.assertIs(result.nav_section, mock_nav_inst)
            self.assertIs(result.param_section, mock_param_inst)
            self.assertIs(result.status_section, mock_status_inst)

            mock_tool_inst.pack.assert_called_once()
            mock_nav_inst.pack.assert_called_once()
            mock_param_inst.pack.assert_called_once()
            mock_status_inst.pack.assert_called_once()
            self.assertEqual(mock_sep_cls.return_value.pack.call_count, 2)


if __name__ == '__main__':
    main()
