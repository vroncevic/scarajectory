# -*- coding: UTF-8 -*-

'''
Module
    controls_panel.py
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

from tkinter import BOTH, Widget
from tkinter.ttk import Frame, Notebook

from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.controls.tabs_bundle import ControlsTabsBundle
from scarajectory.infrastructure.gui.dsl.dsl_editor_tab import DslEditorTab
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab import JogTab
from scarajectory.infrastructure.gui.preview.preview_tab import PreviewTab
from scarajectory.infrastructure.gui.streaming.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.validation.validation_tab import ValidationTab

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
    ) -> None:
        super().__init__(parent)
        self._notebook = Notebook(self)
        self._notebook.pack(fill=BOTH, expand=True)

    @property
    def notebook(self) -> Notebook:
        '''Returns multi-tab notebook container.'''
        return self._notebook

    def mount_tabs(self, tabs: ControlsTabsBundle) -> None:
        '''
            Mounts injected tab subcomponents into notebook.

            :param tabs: Injected ControlsTabsBundle container instance.
        '''
        self._dsl_editor_tab = tabs.dsl_editor_tab
        self._streamer_tab = tabs.streamer_tab
        self._validation_tab = tabs.validation_tab
        self._jog_tab = tabs.jog_tab
        self._preview_tab = tabs.preview_tab

        self._notebook.add(self._dsl_editor_tab, text=' SCARA DSL ')
        self._notebook.add(self._streamer_tab, text=' Hardware Streamer ')
        self._notebook.add(self._validation_tab, text=' Plan Validation ')
        self._notebook.add(self._jog_tab, text=' Manual Jog ')
        self._notebook.add(self._preview_tab, text=' Program Preview ')

    def refresh_ports(self) -> None:
        '''Scans and updates available serial ports.'''
        if hasattr(self, '_streamer_tab'):
            self._streamer_tab.refresh_ports()

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends message to streamer terminal log console.

            :param text: Message string.
            :param is_outgoing: True if message was sent, False if received.
        '''
        if hasattr(self, '_streamer_tab'):
            self._streamer_tab.append_log(text, is_outgoing)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates streamer progress bar and metrics.

            :param progress: StreamProgress model instance.
        '''
        if hasattr(self, '_streamer_tab'):
            self._streamer_tab.update_progress(progress)
