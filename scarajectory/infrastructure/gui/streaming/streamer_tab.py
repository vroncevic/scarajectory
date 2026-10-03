# -*- coding: UTF-8 -*-

'''
Module
    streamer_tab.py
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

from tkinter import BOTH, Widget, X
from tkinter.ttk import Frame

from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.infrastructure.gui.connection.port_connection_panel import PortConnectionPanel
from scarajectory.infrastructure.gui.console.serial_console import SerialConsole
from scarajectory.infrastructure.gui.manipulator.manipulator_override_panel import ManipulatorOverridePanel
from scarajectory.infrastructure.gui.streaming.panel.stream_control_panel import StreamControlPanel
from scarajectory.infrastructure.gui.streaming.panel.stream_progress_adapter import StreamProgressAdapter
from scarajectory.infrastructure.gui.streaming.panel.stream_status_bar import StreamStatusBar
from scarajectory.infrastructure.gui.streaming.streamer_action_bundle import StreamerActionBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerTab(Frame):
    '''
        Hardware connection and trajectory streaming tab container.

        It defines:

            :attributes:
                | _port_panel - Serial port connection subpanel.
                | _status_bar - Status bar rendering active connection info.
                | _progress_adapter - UI adapter synchronizing stream state.
                | _override_panel - Manual manipulator override controls panel.
                | _actions - Mounted playback and tool action handlers bundle.
                | _ctrl_panel - Streaming playback execution control panel.
                | _console - Serial communication terminal output component.
            :methods:
                | __init__ - Initializes the streamer tab panel and sub-widgets.
                | mount_actions - Mounts pre-assembled action handlers and control panel.
                | refresh_ports - Scans available serial/USB ports on the host.
                | append_log - Appends message to terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    _port_panel: PortConnectionPanel
    _status_bar: StreamStatusBar
    _progress_adapter: StreamProgressAdapter
    _override_panel: ManipulatorOverridePanel
    _actions: StreamerActionBundle
    _ctrl_panel: StreamControlPanel
    _console: SerialConsole

    def __init__(
        self,
        parent: Widget,
        *,
        connection_repository: IConnectionRepository,
    ) -> None:
        '''
            Initializes the streamer tab panel and sub-widgets.

            :param parent: Parent notebook widget.
            :param connection_repository: Injected IConnectionRepository instance.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6)

        self._port_panel = PortConnectionPanel(
            self,
            connection_repository=connection_repository,
        )
        self._port_panel.pack(fill=X, pady=2)

        self._status_bar = StreamStatusBar(self)
        self._status_bar.pack(fill=X, pady=2)

        self._progress_adapter = StreamProgressAdapter(
            port_panel=self._port_panel,
            status_bar=self._status_bar,
        )

        self._override_panel = ManipulatorOverridePanel(self)
        self._override_panel.pack(fill=X, pady=2)

    def mount_actions(
        self,
        actions: StreamerActionBundle,
    ) -> None:
        '''
            Mounts pre-assembled action handlers and control panel.

            :param actions: StreamerActionBundle containing action handlers.
            :exceptions: None.
        '''
        self._actions = actions
        self._port_panel.set_connection_delegate(actions.playback_handler)
        self._override_panel.set_action_delegate(actions.tool_handler)

        self._ctrl_panel = StreamControlPanel(
            self,
            control_delegate=actions.playback_handler,
        )
        self._ctrl_panel.pack(fill=X, pady=4)

        self._console = SerialConsole(self)
        self._console.pack(fill=BOTH, expand=True, pady=2)

    @property
    def port_panel(self) -> PortConnectionPanel:
        '''
            Returns port connection panel.

            :return: PortConnectionPanel instance.
            :exceptions: None.
        '''
        return self._port_panel

    @property
    def status_bar(self) -> StreamStatusBar:
        '''
            Returns stream status bar.

            :return: StreamStatusBar instance.
            :exceptions: None.
        '''
        return self._status_bar

    @property
    def progress_adapter(self) -> StreamProgressAdapter:
        '''
            Returns stream progress adapter.

            :return: StreamProgressAdapter instance.
            :exceptions: None.
        '''
        return self._progress_adapter

    @property
    def override_panel(self) -> ManipulatorOverridePanel:
        '''
            Returns manipulator override panel.

            :return: ManipulatorOverridePanel instance.
            :exceptions: None.
        '''
        return self._override_panel

    @property
    def actions(self) -> StreamerActionBundle:
        '''
            Returns mounted action handlers bundle.

            :return: StreamerActionBundle instance.
            :exceptions: None.
        '''
        return self._actions

    @property
    def console(self) -> SerialConsole:
        '''
            Returns serial terminal console component.

            :return: SerialConsole instance.
            :exceptions: None.
        '''
        return self._console

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
