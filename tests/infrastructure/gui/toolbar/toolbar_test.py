# -*- coding: UTF-8 -*-

'''
Module
    toolbar_test.py
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
    Unit tests for Toolbar component.
'''

from __future__ import annotations

from tkinter import Tk, Widget
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle
from scarajectory.infrastructure.gui.toolbar.section.navigation import NavigationSection
from scarajectory.infrastructure.gui.toolbar.section.parameter import ParameterSection
from scarajectory.infrastructure.gui.toolbar.section.status import StatusSection
from scarajectory.infrastructure.gui.toolbar.section.tool import ToolSection
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubSectionsAssembler:
    '''Stub assembler implementing ISectionsAssembler structurally.'''

    def __init__(self, sections: SectionsBundle) -> None:
        self.sections = sections

    def assemble_sections(
        self,
        parent: Widget,
        bundle: ToolbarBundle,
    ) -> SectionsBundle:
        '''
            Returns stubbed sections bundle.

            :param parent: Parent container widget.
            :param bundle: Toolbar bundle.
            :return: Sections bundle.
            :exceptions: None.
        '''
        _ = (parent, bundle)
        return self.sections

    def get_version(self) -> str:
        '''
            Returns version string.

            :return: Version string.
            :exceptions: None.
        '''
        return '1.0.3'


class ToolbarTestCase(TestCase):
    '''
        Test cases verifying Toolbar orchestration and section mounting.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | setUp - Sets up toolbar and mocks.
                | tearDown - Tears down toolbar widget.
                | test_toolbar_version - Verifies toolbar version getter.
                | test_set_deadzone_delegation - Tests deadzone setting delegation.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tk fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down root Tk fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up toolbar and mocks.

            :exceptions: None.
        '''
        self.mock_param = MagicMock(spec=ParameterSection)
        sections = SectionsBundle(
            tool_section=MagicMock(spec=ToolSection),
            nav_section=MagicMock(spec=NavigationSection),
            param_section=self.mock_param,
            status_section=MagicMock(spec=StatusSection),
        )
        assembler = StubSectionsAssembler(sections)
        bundle = MagicMock(spec=ToolbarBundle)
        self.toolbar = Toolbar(self.root, assembler, bundle)

    def tearDown(self) -> None:
        '''
            Tears down toolbar widget.

            :exceptions: None.
        '''
        self.toolbar.destroy()

    def test_toolbar_version(self) -> None:
        '''
            Verifies toolbar version string.

            :exceptions: None.
        '''
        self.assertEqual(self.toolbar.get_version(), '1.0.3')

    def test_set_deadzone_delegation(self) -> None:
        '''
            Tests deadzone setting delegation.

            :exceptions: None.
        '''
        self.toolbar.set_deadzone(False)
        self.mock_param.set_deadzone.assert_called_once_with(False)


if __name__ == '__main__':
    main()
