# -*- coding: UTF-8 -*-

'''
Module
    controls.py
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
    Tabbed control notebook housing Streamer, Validator, Jog and Program preview subcomponents.
'''

from __future__ import annotations

from tkinter import BOTH, Event, Widget
from tkinter.ttk import Frame, Notebook
from typing import Final

from scarajectory.core.model.communication.stream_progress import StreamProgress
from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.iservice import IService
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.communication.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.service.trajectory.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.infrastructure.gui.stream.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.editor.validation_tab import ValidationTab
from scarajectory.infrastructure.gui.stream.jog_tab import JogTab
from scarajectory.infrastructure.gui.editor.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsPanel(Frame):
    '''
        Tabbed controller housing Streamer, Validation, Jog and Program preview panels.

        It defines:

            :attributes:
                | _notebook - Multi-tab notebook container.
                | _dsl_editor_tab - SCARA DSL script editor and compiler tab.
                | _streamer_tab - Serial streaming and logging tab.
                | _validation_tab - Kinematic validation tab.
                | _jog_tab - Manual jog movement and actuator control tab.
                | _preview_tab - ASCII microcontroller program preview tab.
            :methods:
                | __init__ - Initializes tabbed control panels and mounts subcomponents.
                | _on_tab_changed - Handles tab switch event and flushes pending drawing tasks.
                | refresh_ports - Scans and updates available serial ports.
                | append_log - Appends message to streamer terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    _notebook: Notebook
    _dsl_editor_tab: DslEditorTab
    _streamer_tab: StreamerTab
    _validation_tab: ValidationTab
    _jog_tab: JogTab
    _preview_tab: PreviewTab

    def __init__(
        self,
        parent: Widget,
        plan: ITrajectoryPlan,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        storage: IPlanStorageService | None = None,
        dsl_service: IScaraDslService | None = None,
        service: IService | None = None,
        **kwargs: object
    ) -> None:
        '''
            Initializes tabbed control panels and mounts subcomponents.

            :param parent: Parent container widget.
            :param plan: Active ITrajectoryPlan.
            :param validator: ITrajectoryValidator instance.
            :param streamer: ITrajectoryStreamer instance.
            :param storage: Optional IPlanStorageService instance.
            :param dsl_service: Optional IScaraDslService instance.
            :param service: Optional IService instance.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)

        self._notebook = Notebook(self)
        self._notebook.pack(fill=BOTH, expand=True)
        self._notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

        self._dsl_editor_tab: Final[DslEditorTab] = DslEditorTab(
            self._notebook,
            plan=plan,
            validator=validator,
            dsl_service=dsl_service,
            storage=storage
        )
        self._streamer_tab: Final[StreamerTab] = StreamerTab(
            self._notebook,
            plan=plan,
            validator=validator,
            streamer=streamer,
            service=service
        )
        self._validation_tab: Final[ValidationTab] = ValidationTab(
            self._notebook,
            plan=plan,
            validator=validator,
            service=service
        )
        self._jog_tab: Final[JogTab] = JogTab(self._notebook, streamer=streamer)
        self._preview_tab: Final[PreviewTab] = PreviewTab(self._notebook, plan=plan)

        self._notebook.add(self._dsl_editor_tab, text=' SCARA DSL ')
        self._notebook.add(self._streamer_tab, text=' Hardware Streamer ')
        self._notebook.add(self._validation_tab, text=' Plan Validation ')
        self._notebook.add(self._jog_tab, text=' Manual Jog ')
        self._notebook.add(self._preview_tab, text=' Program Preview ')

    def _on_tab_changed(self, event: Event) -> None:
        '''
            Handles tab switch event and forces geometry and drawing synchronization.

            :param event: Tkinter event instance.
            :exceptions: None.
        '''
        self.update_idletasks()

    def refresh_ports(self) -> None:
        '''
            Scans and updates available serial ports.

            :exceptions: None.
        '''
        self._streamer_tab.refresh_ports()

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends message to streamer terminal log console.

            :param text: Message string.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        self._streamer_tab.append_log(text, is_outgoing)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates streamer progress bar and metrics.

            :param progress: StreamProgress model.
            :exceptions: None.
        '''
        self._streamer_tab.update_progress(progress)
