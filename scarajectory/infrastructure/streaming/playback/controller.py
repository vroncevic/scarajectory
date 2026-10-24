# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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
    Coordinates playback lifecycle and execution controls for streaming.
'''

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from math import atan2, degrees, sqrt
from time import time
from typing import Final

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.streaming.playback.dependencies import PlaybackDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlaybackController:
    '''
    Coordinates playback lifecycle and execution controls for streaming.

    It defines:

        :attributes:
            | _deps - Injected PlaybackDependencies collaborator container.
            | _session - Active StreamSession instance.

        :methods:
            | __init__ - Initializes playback controller with injected collaborators.
            | start_streaming - Starts background streaming worker with sequence of waypoints.
            | pause_streaming - Pauses background streaming transmission.
            | resume_streaming - Resumes paused background streaming transmission.
            | stop_streaming - Aborts active streaming session and triggers E-STOP.
    '''

    _deps: PlaybackDependencies
    _session: StreamSession

    def __init__(
        self,
        *,
        dependencies: PlaybackDependencies,
    ) -> None:
        '''
        Initializes playback controller with injected collaborators.

        :param dependencies: Injected PlaybackDependencies container.
        '''
        self._deps: Final[PlaybackDependencies] = dependencies
        self._session: StreamSession = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

    def start_streaming(self, waypoints: Sequence[TrajectoryWaypoint]) -> bool:
        '''
        Starts background streaming worker with sequence of waypoints.

        :param waypoints: Sequence of TrajectoryWaypoint instances.
        :return: True if streaming started, False otherwise.
        '''
        if not self._deps.connection_manager.is_connected():
            self._deps.stream_observer_dispatcher.notify_log(
                '[ERR]: Cannot stream - Transport not connected'
            )
            return False

        if not waypoints:
            return False

        self._session = StreamSession(
            waypoints=list(waypoints),
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=time(),
        )
        self._deps.stream_state_machine.transition_to(StreamState.STREAMING)
        self._deps.flow_barrier_coordinator.reset()

        start_ts: str = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        self._deps.stream_observer_dispatcher.notify_log(
            f'[{start_ts}] [STREAM TRIGGERED]: Starting execution of '
            f'{len(self._session.waypoints)} waypoints...'
        )
        for idx, wp in enumerate(waypoints, start=1):
            r2: float = wp.x * wp.x + wp.y * wp.y
            cos_q2: float = (r2 - 36900.0) / 36000.0
            if -1.0 <= cos_q2 <= 1.0:
                sin_q2: float = sqrt(max(0.0, 1.0 - cos_q2 * cos_q2))
                theta1: float = atan2(wp.y, wp.x) - atan2(120.0 * sin_q2, 150.0 + 120.0 * cos_q2)
                if theta1 < -2.618 or theta1 > 2.618:
                    self._deps.stream_observer_dispatcher.notify_log(
                        f'[{start_ts}] [WARN] Waypoint P{idx} ({wp.x:.1f}, {wp.y:.1f}) requires '
                        f'Lefty elbow configuration (Righty J1 {degrees(theta1):.1f}° exceeds limit).'
                    )

        self._deps.control_transmitter.send_enable()
        self._deps.execution_worker.start_waypoints(session=self._session)
        self._deps.stream_observer_dispatcher.notify_progress(
            state=self._deps.stream_state_machine.state,
            session=self._session,
        )

        return True

    def pause_streaming(self) -> None:
        '''
        Pauses background streaming transmission.
        '''
        if self._deps.stream_state_machine.state == StreamState.STREAMING:
            self._deps.stream_state_machine.transition_to(StreamState.PAUSED)
            self._deps.execution_worker.set_paused(True)
            self._deps.stream_observer_dispatcher.notify_progress(
                state=self._deps.stream_state_machine.state,
                session=self._session,
            )
            self._deps.control_transmitter.send_hold()
            self._deps.stream_observer_dispatcher.notify_log('[HOST]: Streaming PAUSED')

    def resume_streaming(self) -> None:
        '''
        Resumes paused background streaming transmission.
        '''
        if self._deps.stream_state_machine.state == StreamState.PAUSED:
            self._deps.stream_state_machine.transition_to(StreamState.STREAMING)
            self._deps.execution_worker.set_paused(False)
            self._deps.stream_observer_dispatcher.notify_progress(
                state=self._deps.stream_state_machine.state,
                session=self._session,
            )
            self._deps.control_transmitter.send_resume()
            self._deps.stream_observer_dispatcher.notify_log('[HOST]: Streaming RESUMED')

    def stop_streaming(self) -> None:
        '''
        Aborts active streaming session and triggers E-STOP.
        '''
        was_streaming: bool = self._deps.stream_state_machine.is_active()
        self._deps.stream_state_machine.transition_to(StreamState.STOPPED)
        self._deps.execution_worker.stop()

        if self._deps.connection_manager.is_connected():
            self._deps.control_transmitter.send_estop()

        self._deps.stream_observer_dispatcher.notify_progress(
            state=self._deps.stream_state_machine.state,
            session=self._session,
        )

        if was_streaming:
            self._deps.stream_observer_dispatcher.notify_log(
                '[HOST]: Streaming ABORTED (E-STOP sent)'
            )
