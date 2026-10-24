# -*- coding: UTF-8 -*-

'''
Module
    tab.py
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
    Hardware connection and trajectory streaming tab container.
'''

from __future__ import annotations

from tkinter import Widget
from tkinter.ttk import Frame

from scarajectory.core.model.telemetry.progress import StreamProgress
from scarajectory.infrastructure.gui.connection.panel.panel import PortConnectionPanel
from scarajectory.infrastructure.gui.console.panel import SerialConsole
from scarajectory.infrastructure.gui.streaming.progress.adapter import StreamProgressAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTab(Frame):
    '''
        Hardware connection and trajectory streaming tab container.

        It defines:

            :attributes:
                | _port_panel - Serial port connection subpanel.
                | _progress_adapter - UI adapter synchronizing stream state.
                | _console - Serial communication terminal output component.
            :methods:
                | __init__ - Initializes the streamer tab frame container.
                | bind_components - Binds collaborating UI subcomponents.
                | refresh_ports - Scans available serial/USB ports on the host.
                | append_log - Appends message to terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    _port_panel: PortConnectionPanel
    _progress_adapter: StreamProgressAdapter
    _console: SerialConsole

    def __init__(self, parent: Widget) -> None:
        '''
            Initializes the streamer tab frame container.

            :param parent: Parent notebook widget.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6)

    def bind_components(
        self,
        *,
        port_panel: PortConnectionPanel,
        progress_adapter: StreamProgressAdapter,
        console: SerialConsole,
    ) -> None:
        '''
            Binds collaborating UI subcomponents to this tab container.

            :param port_panel: Injected PortConnectionPanel instance.
            :param progress_adapter: Injected StreamProgressAdapter instance.
            :param console: Injected SerialConsole instance.
            :exceptions: None.
        '''
        self._port_panel = port_panel
        self._progress_adapter = progress_adapter
        self._console = console

    def refresh_ports(self) -> None:
        '''
            Scans and lists active serial / tty ports on the host system.

            :exceptions: None.
        '''
        self._port_panel.refresh_ports()

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends timestamped message to the terminal console widget.

            :param text: Message string.
            :param is_outgoing: True if transmitted command.
            :exceptions: None.
        '''
        self._console.append_log(text, is_outgoing)
        self._progress_adapter.handle_log_message(text)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates progress bar and streaming status indicator widgets.

            :param progress: StreamProgress data model.
            :exceptions: None.
        '''
        self._progress_adapter.update_progress(progress)
