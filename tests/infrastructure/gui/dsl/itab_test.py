# -*- coding: UTF-8 -*-

'''
Module
    itab_test.py
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
    Unit tests for IDslEditorTab structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.handler.binary.idelegate import IDslBinaryDelegate
from scarajectory.infrastructure.gui.dsl.handler.execution.idelegate import IDslExecutionDelegate
from scarajectory.infrastructure.gui.dsl.handler.file.idelegate import IDslFileDelegate
from scarajectory.infrastructure.gui.dsl.itab import IDslEditorTab
from scarajectory.infrastructure.gui.dsl.toolbar.itoolbar import IDslEditorToolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidEditorTabMock:
    '''
        Mock conforming structurally to IDslEditorTab.
    '''

    def mount_views(
        self,
        *,
        toolbar: IDslEditorToolbar,
        editor: IDslCodeEditor,
        console: IDslConsoleView,
    ) -> None:
        '''
            Mounts views.
        '''

    def mount_handlers(
        self,
        *,
        execution_handler: IDslExecutionDelegate,
        file_handler: IDslFileDelegate,
        binary_handler: IDslBinaryDelegate,
        store: IWaypointStore,
    ) -> None:
        '''
            Mounts handlers.
        '''

    def load_initial_content(self) -> None:
        '''
            Loads initial content.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.
        '''
        return '1.0.3'


class IncompleteEditorTabMock:
    '''
        Mock missing required protocol methods.
    '''

    def load_initial_content(self) -> None:
        '''
            Loads initial content.
        '''

    def get_name(self) -> str:
        '''
            Returns dummy name to satisfy public methods minimum.
        '''
        return 'incomplete'


class TestIDslEditorTab(TestCase):
    '''
        Tests verifying runtime checkable compliance for IDslEditorTab.
    '''

    def test_valid_implementation_is_instance(self) -> None:
        '''
            Verifies that a valid structural mock satisfies IDslEditorTab.

            :exceptions: None.
        '''
        mock = ValidEditorTabMock()
        self.assertTrue(isinstance(mock, IDslEditorTab))

    def test_incomplete_implementation_fails(self) -> None:
        '''
            Verifies that an incomplete mock fails IDslEditorTab check.

            :exceptions: None.
        '''
        mock = IncompleteEditorTabMock()
        self.assertFalse(isinstance(mock, IDslEditorTab))


if __name__ == '__main__':
    main()
