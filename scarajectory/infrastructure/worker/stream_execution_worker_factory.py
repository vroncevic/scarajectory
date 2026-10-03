# -*- coding: UTF-8 -*-

'''
Module
    stream_execution_worker_factory.py
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
    Factory service constructing StreamExecutionWorker background workers.
'''

from __future__ import annotations

from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.icommand_formatter import ICommandFormatter
from scarajectory.core.service.worker.icommand_sender import ICommandSender
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.worker.stream_execution_worker import StreamExecutionWorker
from scarajectory.infrastructure.worker.stream_loop_runner import StreamLoopRunner
from scarajectory.infrastructure.worker.stream_loop_runner_factory import StreamLoopRunnerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorkerFactory:
    '''
        Factory providing creation of StreamExecutionWorker instances.

        It defines:

            :methods:
                | create - Constructs StreamExecutionWorker with internal default formatter.
                | create_with_formatter - Constructs StreamExecutionWorker with explicit formatter.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        pacing_bundle: FlowPacingBundle,
        command_sender: ICommandSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> StreamExecutionWorker:
        '''
            Constructs and returns a configured StreamExecutionWorker instance.

            :param pacing_bundle: FlowPacingBundle managing pacing and barrier.
            :param command_sender: ICommandSender transmitting raw command packets.
            :param state_controller: IStreamStateController managing stream lifecycle state.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :return: StreamExecutionWorker instance.
            :exceptions: None.
        '''
        loop_runner: StreamLoopRunner = StreamLoopRunnerFactory.create(
            pacing_bundle=pacing_bundle,
            command_sender=command_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

        return StreamExecutionWorker(
            loop_runner=loop_runner,
            barrier_coordinator=pacing_bundle.barrier_coordinator,
        )

    @classmethod
    def create_with_formatter(
        cls,
        *,
        pacing_bundle: FlowPacingBundle,
        formatter: ICommandFormatter,
        command_sender: ICommandSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> StreamExecutionWorker:
        '''
            Constructs and returns a configured StreamExecutionWorker with explicit formatter.

            :param pacing_bundle: FlowPacingBundle managing pacing and barrier.
            :param formatter: ICommandFormatter instance encoding waypoints.
            :param command_sender: ICommandSender transmitting raw command packets.
            :param state_controller: IStreamStateController managing stream lifecycle state.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :return: StreamExecutionWorker instance.
            :exceptions: None.
        '''
        loop_runner: StreamLoopRunner = (
            StreamLoopRunnerFactory.create_with_formatter(
                pacing_bundle=pacing_bundle,
                formatter=formatter,
                command_sender=command_sender,
                state_controller=state_controller,
                observer_dispatcher=observer_dispatcher,
                pacing_config=pacing_config,
            )
        )

        return StreamExecutionWorker(
            loop_runner=loop_runner,
            barrier_coordinator=pacing_bundle.barrier_coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
