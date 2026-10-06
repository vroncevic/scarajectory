# -*- coding: UTF-8 -*-

'''
Module
    ieditor_pane_builder.py
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
    Defines abstract interface for assembling and mounting editor and controls pane.
'''

from __future__ import annotations

from tkinter.ttk import PanedWindow
from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.controls.controls_panel import ControlsPanel
from scarajectory.infrastructure.gui.editor.waypoint_editor import WaypointEditor
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IEditorPaneBuilder(Protocol):
    '''
        Protocol defining contract for constructing and mounting editor pane.

        It defines:

            :methods:
                | build - Constructs right paned container with table and controls.
                | get_version - Returns interface version string.
    '''

    def build(
        self,
        parent: PanedWindow,
        *,
        bundle: ScarajectoryGUIInitBundle,
    ) -> tuple[WaypointEditor, ControlsPanel]:
        '''
            Constructs and mounts right paned container with table and controls.

            :param parent: Parent PanedWindow container.
            :param bundle: GUI initialization dependencies bundle.
            :return: Tuple containing WaypointEditor and ControlsPanel.
        '''

    def get_version(self) -> str:
        '''
            Returns the component version string.

            :return: Component version string.
        '''
