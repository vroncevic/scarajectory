# -*- coding: UTF-8 -*-

'''
Module
    streamer.py
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
    Executes binary compiled programs directly to hardware via streaming pipeline.
'''

from __future__ import annotations

from time import time
from typing import Final

from scaralang.core.model.dsl.binary.program import BinaryProgram

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.streaming.binary.dependencies import BinaryDependencies
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamer:
    '''
        Streams pre-compiled binary DSL programs directly to connected hardware.

        It defines:

            :attributes:
                | _connection_manager - Injected connection state inspector.
                | _state_machine - Stream state machine controller.
                | _dispatcher - Stream observer dispatcher.
                | _worker - Execution worker executing stream loop.
                | _session - Streaming session metrics model.

            :methods:
                | stream_binary_program - Streams pre-compiled BinaryProgram to hardware.
                | is_streaming - Checks if binary streaming session is active.
    '''

    _connection_manager: IConnectionManager
    _state_machine: IStreamStateMachine
    _dispatcher: IStreamObserverDispatcher
    _worker: IExecutionWorker
    _session: StreamSession

    def __init__(
        self,
        dependencies: BinaryDependencies,
    ) -> None:
        '''
            Initializes binary streamer with required collaborators.

            :param dependencies: Injected BinaryDependencies parameter bundle.
            :exceptions: None.
        '''
        self._connection_manager: Final[IConnectionManager] = (
            dependencies.connection_manager
        )
        self._state_machine: Final[IStreamStateMachine] = (
            dependencies.stream_state_machine
        )
        self._dispatcher: Final[IStreamObserverDispatcher] = (
            dependencies.stream_observer_dispatcher
        )
        self._worker: Final[IExecutionWorker] = (
            dependencies.execution_worker
        )
        self._session: Final[StreamSession] = dependencies.session

    def stream_binary_program(self, program: BinaryProgram) -> bool:
        '''
            Streams pre-compiled BinaryProgram directly to hardware.

            :param program: BinaryProgram containing steps and raw frames.
            :return: True if streaming started, False otherwise.
        '''
        if not self._connection_manager.is_connected():
            self._dispatcher.notify_log(
                '[ERR]: Cannot stream - Transport not connected'
            )
            return False

        if not program.steps:
            return False

        self._session.waypoints = []
        self._session.sent_count = 0
        self._session.done_count = 0
        self._session.failed_count = 0
        self._session.remote_queue_depth = 0
        self._session.start_time = time()

        self._state_machine.transition_to(StreamState.STREAMING)

        self._worker.start_program(
            session=self._session,
            program=program,
        )

        self._dispatcher.notify_progress(
            state=self._state_machine.state,
            session=self._session,
        )

        return True

    def is_streaming(self) -> bool:
        '''
            Checks if binary streaming session is currently active.

            :return: True if active, False otherwise.
        '''
        return self._state_machine.is_active()
