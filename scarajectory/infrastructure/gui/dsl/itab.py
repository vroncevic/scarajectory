# -*- coding: UTF-8 -*-

'''
Module
    itab.py
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
    Defines structural protocol IDslEditorTab for DSL editor container tab.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.service.trajectory.plan.store.istore import IWaypointStore
from scarajectory.infrastructure.gui.dsl.console.iconsole import IDslConsoleView
from scarajectory.infrastructure.gui.dsl.editor.ieditor import IDslCodeEditor
from scarajectory.infrastructure.gui.dsl.handler.binary.idelegate import IDslBinaryDelegate
from scarajectory.infrastructure.gui.dsl.handler.execution.idelegate import IDslExecutionDelegate
from scarajectory.infrastructure.gui.dsl.handler.file.idelegate import IDslFileDelegate
from scarajectory.infrastructure.gui.dsl.toolbar.itoolbar import IDslEditorToolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDslEditorTab(Protocol):
    '''
        Structural protocol defining DSL editor container tab operations.

        It defines:

            :methods:
                | mount_views - Mounts and packs toolbar, editor, and console views.
                | mount_handlers - Injects action delegates and waypoint store.
                | load_initial_content - Loads initial plan or demo script into editor.
                | get_version - Returns tab component version string.
    '''

    def mount_views(
        self,
        *,
        toolbar: IDslEditorToolbar,
        editor: IDslCodeEditor,
        console: IDslConsoleView,
    ) -> None:
        '''
            Mounts and packs toolbar, code editor, and console subcomponents.

            :param toolbar: Assembled action toolbar.
            :param editor: Syntax-highlighted code editor.
            :param console: Diagnostic output console.
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
            Injects action delegates and store collaborator.

            :param execution_handler: Delegate handling compilation and execution.
            :param file_handler: Delegate handling file persistence and demo loading.
            :param binary_handler: Delegate handling binary export and import.
            :param store: Waypoint query store.
        '''

    def load_initial_content(self) -> None:
        '''
            Loads either the exported active plan or demonstration script into the editor.
        '''

    def get_version(self) -> str:
        '''
            Returns tab component version string.

            :return: Semantic version string.
        '''
