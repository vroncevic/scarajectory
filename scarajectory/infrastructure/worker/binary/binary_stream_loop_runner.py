# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_loop_runner.py
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
    Executes binary transmission loops for waypoints or binary programs and handles frames.
'''

from __future__ import annotations

from threading import Event
from time import sleep
from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.binary_frame import BinaryFrame

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.binary.binary_loop_runner_bundle import BinaryLoopRunnerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamLoopRunner:
    '''
        Executes binary transmission loops for waypoints or binary programs and handles frames.

        It defines:

            :attributes:
                | _bundle - Injected BinaryLoopRunnerBundle holding collaborators.
            :methods:
                | __init__ - Initializes loop runner with injected bundle.
                | run_waypoints_loop - Background loop streaming sequence of waypoints.
                | run_program_loop - Background loop streaming pre-compiled binary steps.
                | handle_incoming_bytes - Feeds raw incoming bytes and dispatches frames.
    '''

    _bundle: BinaryLoopRunnerBundle

    def __init__(self, bundle: BinaryLoopRunnerBundle) -> None:
        '''
            Initializes binary stream loop runner with collaborators bundle.

            :param bundle: BinaryLoopRunnerBundle containing collaborators.
            :exceptions: None.
        '''
        self._bundle: Final[BinaryLoopRunnerBundle] = bundle

    def run_waypoints_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Streams sequence of raw waypoints converted to binary frames.

            :param session: Active StreamSession tracking waypoints and progress.
            :param stop_event: Event signaling loop termination.
            :param pause_event: Event signaling transmission pause.
            :exceptions: None.
        '''
        total_pts: int = len(session.waypoints)

        while not stop_event.is_set() and session.sent_count < total_pts:
            if pause_event.is_set():
                sleep(self._bundle.pacing_config.poll_delay)
                continue

            if self._bundle.step_dispatcher.can_dispatch_step(session):
                self._bundle.step_dispatcher.dispatch_waypoint(session)
                sleep(self._bundle.pacing_config.send_delay)
            else:
                sleep(self._bundle.pacing_config.throttle_delay)

        if not stop_event.is_set():
            self._bundle.queue_drainer.drain_queue(
                session=session,
                total_items=total_pts,
                stop_event=stop_event,
            )

    def run_program_loop(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''
            Streams pre-compiled binary steps directly to hardware.

            :param session: Active StreamSession tracking stream metrics.
            :param program: BinaryProgram containing compiled binary steps.
            :param stop_event: Event signaling loop termination.
            :param pause_event: Event signaling transmission pause.
            :exceptions: None.
        '''
        steps: tuple[Step, ...] = program.steps
        total_items: int = len(steps)

        while not stop_event.is_set() and session.sent_count < total_items:
            if pause_event.is_set():
                sleep(self._bundle.pacing_config.poll_delay)
                continue

            if self._bundle.step_dispatcher.can_dispatch_step(session):
                self._bundle.step_dispatcher.dispatch_binary_step(
                    session=session,
                    step=steps[session.sent_count],
                )
                sleep(self._bundle.pacing_config.send_delay)
            else:
                sleep(self._bundle.pacing_config.throttle_delay)

        if not stop_event.is_set():
            self._bundle.queue_drainer.drain_queue(
                session=session,
                total_items=total_items,
                stop_event=stop_event,
            )

    def handle_incoming_bytes(
        self,
        *,
        data: bytes,
        session: StreamSession,
    ) -> bool:
        '''
            Feeds raw incoming bytes into parser and dispatches inbound frames.

            :param data: Byte chunk received from transport.
            :param session: Active StreamSession tracking metrics.
            :return: True if a fault occurred requiring immediate stop, False otherwise.
            :exceptions: None.
        '''
        frames: tuple[BinaryFrame, ...] = self._bundle.frame_parser.feed_bytes(
            data
        )
        should_stop: bool = False

        for frame in frames:
            if self._bundle.frame_handler.handle_frame(frame, session):
                should_stop = True

        return should_stop
