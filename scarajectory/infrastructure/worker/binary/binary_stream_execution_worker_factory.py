# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_execution_worker_factory.py
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
    Factory constructing BinaryStreamExecutionWorker instances.
'''

from __future__ import annotations

from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.packet.ipacket_strategy import IPacketStrategy
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.ibyte_sender import IByteSender
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.worker.binary.binary_stream_execution_worker import BinaryStreamExecutionWorker
from scarajectory.infrastructure.worker.binary.binary_stream_loop_runner_factory import BinaryStreamLoopRunnerFactory
from scarajectory.infrastructure.worker.binary.ibinary_stream_loop_runner import IBinaryStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamExecutionWorkerFactory:
    '''
        Factory constructing BinaryStreamExecutionWorker instances with configured collaborators.

        It defines:

            :methods:
                | create - Constructs BinaryStreamExecutionWorker with internal frame parser.
                | create_with_parser - Constructs BinaryStreamExecutionWorker with injected frame parser.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        pacing_bundle: FlowPacingBundle,
        packet_strategy: IPacketStrategy,
        byte_sender: IByteSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> BinaryStreamExecutionWorker:
        '''
            Constructs BinaryStreamExecutionWorker with internal frame parser.

            :param pacing_bundle: FlowPacingBundle instance holding pacing and barrier.
            :param packet_strategy: IPacketStrategy instance.
            :param byte_sender: IByteSender transmitting raw byte payloads.
            :param state_controller: IStreamStateController managing stream lifecycle state.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :return: BinaryStreamExecutionWorker instance.
            :exceptions: None.
        '''
        loop_runner: IBinaryStreamLoopRunner = BinaryStreamLoopRunnerFactory.create(
            flow_pacing=pacing_bundle.pacing_controller,
            packet_strategy=packet_strategy,
            byte_sender=byte_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

        return BinaryStreamExecutionWorker(
            loop_runner=loop_runner,
            barrier_coordinator=pacing_bundle.barrier_coordinator,
        )

    @classmethod
    def create_with_parser(
        cls,
        *,
        pacing_bundle: FlowPacingBundle,
        packet_strategy: IPacketStrategy,
        frame_parser: BinaryFrameParser,
        byte_sender: IByteSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> BinaryStreamExecutionWorker:
        '''
            Constructs BinaryStreamExecutionWorker with injected frame parser.

            :param pacing_bundle: FlowPacingBundle instance holding pacing and barrier.
            :param packet_strategy: IPacketStrategy instance.
            :param frame_parser: BinaryFrameParser instance.
            :param byte_sender: IByteSender transmitting raw byte payloads.
            :param state_controller: IStreamStateController managing stream lifecycle state.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :return: BinaryStreamExecutionWorker instance.
            :exceptions: None.
        '''
        loop_runner: IBinaryStreamLoopRunner = (
            BinaryStreamLoopRunnerFactory.create_with_parser(
                flow_pacing=pacing_bundle.pacing_controller,
                packet_strategy=packet_strategy,
                frame_parser=frame_parser,
                byte_sender=byte_sender,
                state_controller=state_controller,
                observer_dispatcher=observer_dispatcher,
                pacing_config=pacing_config,
            )
        )

        return BinaryStreamExecutionWorker(
            loop_runner=loop_runner,
            barrier_coordinator=pacing_bundle.barrier_coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
