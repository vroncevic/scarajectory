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

import tkinter as tk
from tkinter import ttk
from typing import Final

from scarajectory.core.model.stream_progress import StreamProgress
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.gui.components.streamer_tab import StreamerTab
from scarajectory.infrastructure.gui.components.validation_tab import ValidationTab
from scarajectory.infrastructure.gui.components.jog_tab import JogTab
from scarajectory.infrastructure.gui.components.preview_tab import PreviewTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsPanel(ttk.Frame):
    '''
        Tabbed controller housing Streamer, Validation, Jog and Program preview panels.

        It defines:

            :attributes:
                | _notebook - Multi-tab notebook container.
                | _streamer_tab - Serial streaming and logging tab.
                | _validation_tab - Kinematic validation tab.
                | _jog_tab - Manual jog movement and actuator control tab.
                | _preview_tab - ASCII microcontroller program preview tab.
            :methods:
                | __init__ - Initializes tabbed control panels and mounts subcomponents.
                | refresh_ports - Scans and updates available serial ports.
                | append_log - Appends message to streamer terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    _notebook: ttk.Notebook
    _streamer_tab: StreamerTab
    _validation_tab: ValidationTab
    _jog_tab: JogTab
    _preview_tab: PreviewTab

    def __init__(
        self,
        parent: tk.Widget,
        plan: TrajectoryPlan,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        **kwargs: object
    ) -> None:
        '''
            Initializes tabbed control panels and mounts subcomponents.

            :param parent: Parent container widget.
            :param plan: Active TrajectoryPlan.
            :param validator: ITrajectoryValidator instance.
            :param streamer: ITrajectoryStreamer instance.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)

        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._streamer_tab: Final[StreamerTab] = StreamerTab(self._notebook, plan=plan, validator=validator, streamer=streamer)
        self._validation_tab: Final[ValidationTab] = ValidationTab(self._notebook, plan=plan, validator=validator)
        self._jog_tab: Final[JogTab] = JogTab(self._notebook, streamer=streamer)
        self._preview_tab: Final[PreviewTab] = PreviewTab(self._notebook, plan=plan)

        self._notebook.add(self._streamer_tab, text=' Hardware Streamer ')
        self._notebook.add(self._validation_tab, text=' Plan Validation ')
        self._notebook.add(self._jog_tab, text=' Manual Jog ')
        self._notebook.add(self._preview_tab, text=' Program Preview ')

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
