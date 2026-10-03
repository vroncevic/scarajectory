# -*- coding: UTF-8 -*-

'''
Module
    stream_loop_runner_factory.py
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
    Factory service constructing StreamLoopRunner with injected collaborators.
'''

from __future__ import annotations

from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.icommand_formatter import ICommandFormatter
from scarajectory.core.service.worker.icommand_sender import ICommandSender
from scarajectory.infrastructure.formatter.command_formatter_factory import CommandFormatterFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.worker.istream_queue_drainer import IStreamQueueDrainer
from scarajectory.infrastructure.worker.istream_step_dispatcher import IStreamStepDispatcher
from scarajectory.infrastructure.worker.stream_loop_runner import StreamLoopRunner
from scarajectory.infrastructure.worker.stream_queue_drainer_factory import StreamQueueDrainerFactory
from scarajectory.infrastructure.worker.stream_step_dispatcher_factory import StreamStepDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLoopRunnerFactory:
    '''
        Factory providing creation of StreamLoopRunner instances.

        It defines:

            :methods:
                | create - Constructs StreamLoopRunner with default formatter.
                | create_with_formatter - Constructs runner with formatter.
                | create_with_collaborators - Constructs runner with delegates.
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
    ) -> StreamLoopRunner:
        '''
            Constructs and returns a configured StreamLoopRunner instance.

            :param pacing_bundle: FlowPacingBundle holding pacing and barrier.
            :param command_sender: Sender transmitting raw command packets.
            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher emitting progress and logs.
            :param pacing_config: Pacing configuration with delays.
            :return: Configured StreamLoopRunner instance.
            :exceptions: None.
        '''
        formatter: ICommandFormatter = CommandFormatterFactory.create()

        return cls.create_with_formatter(
            pacing_bundle=pacing_bundle,
            formatter=formatter,
            command_sender=command_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
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
    ) -> StreamLoopRunner:
        '''
            Constructs and returns StreamLoopRunner with custom formatter.

            :param pacing_bundle: FlowPacingBundle holding pacing and barrier.
            :param formatter: Formatter instance encoding waypoints.
            :param command_sender: Sender transmitting raw command packets.
            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher emitting progress and logs.
            :param pacing_config: Pacing configuration with delays.
            :return: Configured StreamLoopRunner instance.
            :exceptions: None.
        '''
        step_dispatcher = StreamStepDispatcherFactory.create(
            pacing_bundle=pacing_bundle,
            formatter=formatter,
            command_sender=command_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
        )
        queue_drainer = StreamQueueDrainerFactory.create(
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

        return StreamLoopRunner(
            flow_pacing=pacing_bundle.pacing_controller,
            step_dispatcher=step_dispatcher,
            queue_drainer=queue_drainer,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

    @classmethod
    def create_with_collaborators(
        cls,
        *,
        flow_pacing: IFlowPacingController,
        step_dispatcher: IStreamStepDispatcher,
        queue_drainer: IStreamQueueDrainer,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> StreamLoopRunner:
        '''
            Constructs StreamLoopRunner with explicit delegate collaborators.

            :param flow_pacing: IFlowPacingController managing buffer queue.
            :param step_dispatcher: Step dispatcher delegate instance.
            :param queue_drainer: Queue drainer delegate instance.
            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher emitting progress and logs.
            :param pacing_config: Pacing configuration with delays.
            :return: Configured StreamLoopRunner instance.
            :exceptions: None.
        '''
        return StreamLoopRunner(
            flow_pacing=flow_pacing,
            step_dispatcher=step_dispatcher,
            queue_drainer=queue_drainer,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
