# -*- coding: UTF-8 -*-

'''
Module
    stream_playback_action_handler.py
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
    Action handler coordinating stream connection, validation dialogs, and playback flow.
'''

from __future__ import annotations

from tkinter.messagebox import askyesno, showerror
from typing import Final

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.core.service.connection.istream_connection import IStreamConnection
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.infrastructure.gui.connection.port_connection_panel import PortConnectionPanel
from scarajectory.infrastructure.gui.streaming.handler.playback_handler_bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.panel.stream_progress_adapter import StreamProgressAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPlaybackActionHandler:
    '''
        Action handler coordinating stream connection, validation dialogs, and playback flow.

        It defines:

            :attributes:
                | _plan - Active trajectory plan read-only abstraction.
                | _validator - Kinematic reachability validator.
                | _connection - Stream transport connection controller.
                | _playback_controller - Motion trajectory playback controller.
                | _progress_adapter - UI adapter synchronizing stream state.
                | _port_panel - Serial port connection subpanel.
            :methods:
                | __init__ - Initializes playback action handler with collaborators.
                | toggle_connection - Connects or disconnects from selected serial port.
                | on_start_stream - Validates plan and initiates trajectory stream.
                | on_pause_resume_stream - Toggles stream pause/resume state.
                | on_stop_stream - Stops active streaming transmission immediately.
    '''

    _plan: ITrajectoryReadOnly
    _validator: ITrajectoryValidator
    _connection: IStreamConnection
    _playback_controller: IStreamPlaybackController
    _progress_adapter: StreamProgressAdapter
    _port_panel: PortConnectionPanel

    def __init__(
        self,
        *,
        bundle: PlaybackHandlerBundle,
    ) -> None:
        '''
            Initializes playback action handler with presentation and service collaborators.

            :param bundle: Injected PlaybackHandlerBundle container.
            :exceptions: None.
        '''
        self._plan: Final[ITrajectoryReadOnly] = bundle.plan
        self._validator: Final[ITrajectoryValidator] = bundle.validator
        self._connection: Final[IStreamConnection] = bundle.connection
        self._playback_controller: Final[IStreamPlaybackController] = (
            bundle.playback_controller
        )
        self._progress_adapter: Final[StreamProgressAdapter] = bundle.progress_adapter
        self._port_panel: Final[PortConnectionPanel] = bundle.port_panel

    def toggle_connection(self) -> None:
        '''
            Connects or disconnects from selected serial port.

            :exceptions: None.
        '''
        if self._connection.is_connected():
            self._connection.disconnect()
            self._progress_adapter.set_disconnected()
        else:
            port: str = self._port_panel.get_selected_port()

            if not port:
                showerror('Serial Port Error', 'No serial port selected.')
                return

            config: StreamConfig = StreamConfig(
                port=port,
                baudrate=115200,
                timeout=0.1,
                queue_capacity=16,
                protocol_mode=ProtocolMode.BINARY,
            )

            if self._connection.connect_with_config(config):
                self._progress_adapter.set_connected(port)

    def on_start_stream(self) -> None:
        '''
            Validates plan and initiates trajectory stream transmission.

            :exceptions: None.
        '''
        valid, msgs = self._validator.validate_plan(self._plan)

        if not valid:
            res: bool = askyesno(
                'Validation Warnings',
                'Plan has validation warnings/errors:\n\n'
                + '\n'.join(msgs[:4])
                + '\n\nDo you want to proceed anyway?',
            )

            if not res:
                return

        started: bool = self._playback_controller.start_streaming(
            self._plan.waypoints
        )
        if not started:
            showerror(
                'Stream Error',
                'Failed to start stream. Check serial connection.',
            )

    def on_pause_resume_stream(self) -> None:
        '''
            Toggles stream pause/resume state.

            :exceptions: None.
        '''
        try:
            self._playback_controller.pause_streaming()

        except (AttributeError, RuntimeError):
            self._playback_controller.resume_streaming()

    def on_stop_stream(self) -> None:
        '''
            Stops active streaming transmission immediately.

            :exceptions: None.
        '''
        self._playback_controller.stop_streaming()
