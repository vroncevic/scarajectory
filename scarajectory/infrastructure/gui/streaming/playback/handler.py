# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
from typing import ClassVar, Final

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.gui.streaming.playback.bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.status.istatus_bar import IStreamStatusBar
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPlaybackActionHandler:
    '''
        Action handler coordinating stream connection, validation dialogs, and playback flow.

        It defines:

            :attributes:
                | CANONICAL_HOME_X - Canonical robot home position X in mm.
                | CANONICAL_HOME_Y - Canonical robot home position Y in mm.
                | _plan - Active trajectory plan read-only abstraction.
                | _validator - Kinematic reachability validator.
                | _avoidance_adapter - Dead zone avoidance and detour planner adapter.
                | _connection_manager - Stream transport connection controller.
                | _playback_controller - Motion trajectory playback controller.
                | _status_bar - Streaming status and metrics bar protocol.
            :methods:
                | __init__ - Initializes playback action handler with collaborators.
                | toggle_connection - Connects or disconnects from selected serial port.
                | is_connected - Checks if serial connection is currently active.
                | on_start_stream - Validates plan and initiates trajectory stream.
                | on_pause_resume_stream - Toggles stream pause/resume state.
                | on_stop_stream - Stops active streaming transmission immediately.
    '''

    CANONICAL_HOME_X: ClassVar[float] = 13.934
    CANONICAL_HOME_Y: ClassVar[float] = -106.066

    _plan: IWaypointQuery
    _validator: ITrajectoryValidator
    _avoidance_adapter: IDeadZoneAvoidanceAdapter
    _connection_manager: IConnectionManager
    _playback_controller: IPlaybackController
    _status_bar: IStreamStatusBar

    def __init__(
        self,
        *,
        bundle: PlaybackHandlerBundle,
    ) -> None:
        '''
            Initializes playback action handler with collaborators.

            :param bundle: Injected PlaybackHandlerBundle container.
            :exceptions: None.
        '''
        self._plan: Final[IWaypointQuery] = bundle.plan
        self._validator: Final[ITrajectoryValidator] = bundle.validator
        self._avoidance_adapter: Final[IDeadZoneAvoidanceAdapter] = bundle.avoidance_adapter
        self._connection_manager: Final[IConnectionManager] = bundle.connection_manager
        self._playback_controller: Final[IPlaybackController] = bundle.playback_controller
        self._status_bar: Final[IStreamStatusBar] = bundle.status_bar

    def toggle_connection(self, port: str = '') -> None:
        '''
            Connects or disconnects from selected serial port.

            :param port: Optional communication port identifier.
            :exceptions: None.
        '''
        if self._connection_manager.is_connected():
            self._connection_manager.disconnect()
            self._status_bar.set_status_text('Streamer: Disconnected')
            return

        target_port: str = port.strip()

        if not target_port:
            showerror('Serial Port Error', 'No serial port selected.')
            return

        config = StreamConfig(
            port=target_port,
            baudrate=115200,
            timeout=0.1,
            queue_capacity=16,
        )

        if self._connection_manager.connect_with_config(config):
            self._status_bar.set_status_text(f'Streamer: Connected to {target_port}')

    def is_connected(self) -> bool:
        '''
            Checks if serial connection is currently active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._connection_manager.is_connected()

    def on_start_stream(self) -> None:
        '''
            Validates plan and initiates trajectory stream.

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

        waypoints: list[TrajectoryWaypoint] = list(self._plan.waypoints)
        if waypoints:
            home_wp = TrajectoryWaypoint(
                x=self.CANONICAL_HOME_X,
                y=self.CANONICAL_HOME_Y,
                z=waypoints[0].z,
                speed=waypoints[0].speed,
                phi=waypoints[0].phi,
                name='home',
                command='',
            )
            resolved_waypoints: list[TrajectoryWaypoint] = []
            if self._avoidance_adapter.crosses_dead_zone(home_wp, waypoints[0]):
                resolved_waypoints.extend(
                    self._avoidance_adapter.plan_detour(home_wp, waypoints[0])
                )
            else:
                resolved_waypoints.append(waypoints[0])

            for idx in range(1, len(waypoints)):
                prev_wp = resolved_waypoints[-1]
                curr_wp = waypoints[idx]
                if self._avoidance_adapter.crosses_dead_zone(prev_wp, curr_wp):
                    detour = self._avoidance_adapter.plan_detour(prev_wp, curr_wp)
                    resolved_waypoints.extend(detour)
                else:
                    resolved_waypoints.append(curr_wp)

            waypoints = resolved_waypoints

        started: bool = self._playback_controller.start_streaming(waypoints)
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
        except RuntimeError:
            self._playback_controller.resume_streaming()

    def on_stop_stream(self) -> None:
        '''
            Stops active streaming transmission immediately.

            :exceptions: None.
        '''
        self._playback_controller.stop_streaming()
