# -*- coding: UTF-8 -*-

'''
Module
    editor_pane_builder.py
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
    Builder assembling and mounting the right paned editor and controls layout.
'''

from __future__ import annotations

from tkinter import BOTH, VERTICAL
from tkinter.ttk import Frame, PanedWindow
from typing import Final

from scarajectory.infrastructure.gui.controls.bundle import ControlsBundle
from scarajectory.infrastructure.gui.controls.controls_panel import ControlsPanel
from scarajectory.infrastructure.gui.controls.controls_panel_factory import ControlsPanelFactory
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.waypoint_editor import WaypointEditor
from scarajectory.infrastructure.gui.scarajectory_gui_init_bundle import ScarajectoryGUIInitBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class EditorPaneBuilder:
    '''
        Assembles and mounts the right pane containing table editor and controls.

        It defines:

            :attributes:
                | _controls_factory - Injected factory type for controls panel creation.
            :methods:
                | __init__ - Initializes EditorPaneBuilder with factory collaborator.
                | build - Constructs right paned container with table and controls.
                | get_version - Returns builder version string.
    '''

    _controls_factory: type[ControlsPanelFactory]

    def __init__(
        self,
        *,
        controls_factory: type[ControlsPanelFactory] = ControlsPanelFactory,
    ) -> None:
        '''
            Initializes EditorPaneBuilder with injected factory collaborator.

            :param controls_factory: ControlsPanelFactory class or substitute.
            :exceptions: None.
        '''
        self._controls_factory: Final[type[ControlsPanelFactory]] = (
            controls_factory
        )

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
            :exceptions: None.
        '''
        right_frame = Frame(parent)
        parent.add(right_frame, weight=2)
        right_paned = PanedWindow(right_frame, orient=VERTICAL)
        right_paned.pack(fill=BOTH, expand=True)

        table_bundle = TableBundle(
            store=bundle.plan.store,
            selection=bundle.plan.selection,
            mutation=bundle.plan.mutation,
            dispatcher=bundle.plan.dispatcher,
        )
        table = WaypointEditor(right_paned, bundle=table_bundle)
        right_paned.add(table, weight=1)

        ctl_frame = Frame(right_paned)
        right_paned.add(ctl_frame, weight=1)
        controls_bundle = ControlsBundle(
            store=bundle.plan.store,
            mutation=bundle.plan.mutation,
            validator=bundle.validator,
            streaming=bundle.streaming,
            storage=bundle.storage,
            dsl_service=bundle.dsl_service,
            connection_repository=bundle.connection_repository,
        )
        controls = self._controls_factory.create(
            ctl_frame, bundle=controls_bundle
        )
        controls.pack(fill=BOTH, expand=True)

        return table, controls

    def get_version(self) -> str:
        '''
            Returns the builder version string.

            :return: Builder version string.
            :exceptions: None.
        '''
        return __version__
