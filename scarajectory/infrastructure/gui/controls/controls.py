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

from scarajectory.core.model.communication.stream.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.editor.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.editor.validation_tab import ValidationTab
from scarajectory.infrastructure.gui.stream.jog_tab import JogTab
from scarajectory.infrastructure.gui.stream.streamer_tab import StreamerTab

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
                | __init__ - Initializes tabbed container frame.
                | mount_tabs - Mounts injected tab subcomponents into notebook.
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
        **kwargs: object
    ) -> None:
        super().__init__(parent, **kwargs)
        self._notebook = Notebook(self)
        self._notebook.pack(fill=BOTH, expand=True)
        self._notebook.bind('<<NotebookTabChanged>>', self._on_tab_changed)

    @property
    def notebook(self) -> Notebook:
        return self._notebook

    def mount_tabs(
        self,
        *,
        dsl_editor_tab: DslEditorTab,
        streamer_tab: StreamerTab,
        validation_tab: ValidationTab,
        jog_tab: JogTab,
        preview_tab: PreviewTab,
    ) -> None:
        self._dsl_editor_tab = dsl_editor_tab
        self._streamer_tab = streamer_tab
        self._validation_tab = validation_tab
        self._jog_tab = jog_tab
        self._preview_tab = preview_tab

        self._notebook.add(self._dsl_editor_tab, text=' SCARA DSL ')
        self._notebook.add(self._streamer_tab, text=' Hardware Streamer ')
        self._notebook.add(self._validation_tab, text=' Plan Validation ')
        self._notebook.add(self._jog_tab, text=' Manual Jog ')
        self._notebook.add(self._preview_tab, text=' Program Preview ')

    def _on_tab_changed(self, event: Event) -> None:
        self.update_idletasks()

    def refresh_ports(self) -> None:
        if hasattr(self, '_streamer_tab'):
            self._streamer_tab.refresh_ports()

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        if hasattr(self, '_streamer_tab'):
            self._streamer_tab.append_log(text, is_outgoing)

    def update_progress(self, progress: StreamProgress) -> None:
        if hasattr(self, '_streamer_tab'):
            self._streamer_tab.update_progress(progress)
