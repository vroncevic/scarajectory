# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for SectionsBundle container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle
from scarajectory.infrastructure.gui.toolbar.section.navigation import NavigationSection
from scarajectory.infrastructure.gui.toolbar.section.parameter import ParameterSection
from scarajectory.infrastructure.gui.toolbar.section.status import StatusSection
from scarajectory.infrastructure.gui.toolbar.section.tool import ToolSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SectionsBundleTestCase(TestCase):
    '''
        Test cases verifying SectionsBundle creation and immutability.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle with attributes.
                | test_bundle_immutability - Verifies frozen immutability behavior.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Tests creating bundle with attributes.

            :exceptions: None.
        '''
        mock_tool = MagicMock(spec=ToolSection)
        mock_nav = MagicMock(spec=NavigationSection)
        mock_param = MagicMock(spec=ParameterSection)
        mock_status = MagicMock(spec=StatusSection)
        bundle = SectionsBundle(
            tool_section=mock_tool,
            nav_section=mock_nav,
            param_section=mock_param,
            status_section=mock_status,
        )
        self.assertIs(bundle.tool_section, mock_tool)
        self.assertIs(bundle.nav_section, mock_nav)
        self.assertIs(bundle.param_section, mock_param)
        self.assertIs(bundle.status_section, mock_status)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies frozen immutability behavior.

            :exceptions: None.
        '''
        bundle = SectionsBundle(
            tool_section=MagicMock(spec=ToolSection),
            nav_section=MagicMock(spec=NavigationSection),
            param_section=MagicMock(spec=ParameterSection),
            status_section=MagicMock(spec=StatusSection),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.tool_section = MagicMock(spec=ToolSection)  # type: ignore[misc]


if __name__ == '__main__':
    main()
