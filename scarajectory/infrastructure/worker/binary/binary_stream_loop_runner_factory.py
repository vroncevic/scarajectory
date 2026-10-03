# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_loop_runner_factory.py
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
    Factory constructing BinaryStreamLoopRunner instances.
'''

from __future__ import annotations

from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.core.service.packet.ipacket_strategy import IPacketStrategy
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.core.service.worker.ibyte_sender import IByteSender
from scarajectory.infrastructure.worker.binary.binary_stream_frame_handler_factory import BinaryStreamFrameHandlerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_loop_runner import BinaryStreamLoopRunner
from scarajectory.infrastructure.worker.binary.ibinary_stream_frame_handler import IBinaryStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamLoopRunnerFactory:
    '''
        Factory constructing BinaryStreamLoopRunner instances.

        It defines:

            :methods:
                | create - Constructs BinaryStreamLoopRunner with internal parser.
                | create_with_parser - Constructs BinaryStreamLoopRunner with injected parser.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        flow_pacing: IFlowPacingController,
        packet_strategy: IPacketStrategy,
        byte_sender: IByteSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> BinaryStreamLoopRunner:
        '''
            Constructs BinaryStreamLoopRunner with internal frame parser.

            :param flow_pacing: IFlowPacingController managing buffer queue.
            :param packet_strategy: IPacketStrategy encoding waypoints.
            :param byte_sender: IByteSender transmitting raw byte stream.
            :param state_controller: IStreamStateController managing stream lifecycle.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :return: BinaryStreamLoopRunner instance.
            :exceptions: None.
        '''
        frame_handler: IBinaryStreamFrameHandler = (
            BinaryStreamFrameHandlerFactory.create(
                flow_pacing=flow_pacing,
                state_controller=state_controller,
                observer_dispatcher=observer_dispatcher,
            )
        )

        return BinaryStreamLoopRunner(
            flow_pacing=flow_pacing,
            packet_strategy=packet_strategy,
            frame_parser=BinaryFrameParserFactory.create(),
            frame_handler=frame_handler,
            byte_sender=byte_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

    @classmethod
    def create_with_parser(
        cls,
        *,
        flow_pacing: IFlowPacingController,
        packet_strategy: IPacketStrategy,
        frame_parser: BinaryFrameParser,
        byte_sender: IByteSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
        pacing_config: StreamPacingConfig,
    ) -> BinaryStreamLoopRunner:
        '''
            Constructs BinaryStreamLoopRunner with injected frame parser.

            :param flow_pacing: IFlowPacingController managing buffer queue.
            :param packet_strategy: IPacketStrategy encoding waypoints.
            :param frame_parser: BinaryFrameParser decoding inbound frames.
            :param byte_sender: IByteSender transmitting raw byte stream.
            :param state_controller: IStreamStateController managing stream lifecycle.
            :param observer_dispatcher: IStreamObserverDispatcher emitting progress and logs.
            :param pacing_config: StreamPacingConfig with loop pacing delays.
            :return: BinaryStreamLoopRunner instance.
            :exceptions: None.
        '''
        frame_handler: IBinaryStreamFrameHandler = (
            BinaryStreamFrameHandlerFactory.create(
                flow_pacing=flow_pacing,
                state_controller=state_controller,
                observer_dispatcher=observer_dispatcher,
            )
        )

        return BinaryStreamLoopRunner(
            flow_pacing=flow_pacing,
            packet_strategy=packet_strategy,
            frame_parser=frame_parser,
            frame_handler=frame_handler,
            byte_sender=byte_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
