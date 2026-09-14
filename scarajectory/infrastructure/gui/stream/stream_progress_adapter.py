# -*- coding: UTF-8 -*-

'''
Module
    stream_progress_adapter.py
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
    Dedicated progress adapter and connection state synchronizer for streamer UI.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.communication.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.stream.port_connection_panel import PortConnectionPanel
from scarajectory.infrastructure.gui.stream.stream_status_bar import StreamStatusBar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamProgressAdapter:
    '''
        Adapter coordinating streaming metrics, logs, and port connection indicators.

        It defines:

            :attributes:
                | _port_panel - Port connection control panel.
                | _status_bar - Streaming status and metrics bar.
            :methods:
                | __init__ - Initializes the adapter with port panel and status bar.
                | update_progress - Forwards progress data model to the status bar widget.
                | handle_log_message - Inspects log messages for disconnection detection.
                | set_connected - Synchronizes UI controls to connected state.
                | set_disconnected - Synchronizes UI controls to disconnected state.
    '''

    _port_panel: Final[PortConnectionPanel]
    _status_bar: Final[StreamStatusBar]

    def __init__(
        self,
        port_panel: PortConnectionPanel,
        status_bar: StreamStatusBar,
    ) -> None:
        '''
            Initializes the adapter with port panel and status bar.

            :param port_panel: PortConnectionPanel instance.
            :param status_bar: StreamStatusBar instance.
            :exceptions: None.
        '''
        self._port_panel = port_panel
        self._status_bar = status_bar

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Forwards progress data model to the status bar widget.

            :param progress: StreamProgress data model.
            :exceptions: None.
        '''
        self._status_bar.update_progress(progress)

    def handle_log_message(self, text: str) -> None:
        '''
            Inspects log messages for disconnection detection and updates indicators.

            :param text: Message string received from transport or hardware.
            :exceptions: None.
        '''
        if 'Connection lost' in text or 'Disconnected from' in text:
            self.set_disconnected()
        elif 'Connected to ' in text and not text.startswith('>>>'):
            parts = text.split('Connected to ')

            if len(parts) > 1:
                target = parts[1].split(' ')[0]
                self.set_connected(target)

    def set_connected(self, port: str) -> None:
        '''
            Synchronizes UI controls to connected state.

            :param port: Connected serial port identifier.
            :exceptions: None.
        '''
        self._port_panel.save_preference()
        self._port_panel.set_connected_state(True)
        self._status_bar.set_status_text(f'Streamer: Connected to {port}')

    def set_disconnected(self) -> None:
        '''
            Synchronizes UI controls to disconnected state.

            :exceptions: None.
        '''
        self._port_panel.set_connected_state(False)
        self._status_bar.set_status_text('Streamer: Disconnected')
