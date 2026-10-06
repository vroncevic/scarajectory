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

from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory

from scarajectory.infrastructure.worker.binary.binary_loop_runner_bundle import BinaryLoopRunnerBundle
from scarajectory.infrastructure.worker.binary.binary_queue_drainer_factory import BinaryQueueDrainerFactory
from scarajectory.infrastructure.worker.binary.binary_step_bundle import BinaryStepBundle
from scarajectory.infrastructure.worker.binary.binary_step_dispatcher_factory import BinaryStepDispatcherFactory
from scarajectory.infrastructure.worker.binary.binary_stream_frame_handler_factory import BinaryStreamFrameHandlerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_loop_runner import BinaryStreamLoopRunner
from scarajectory.infrastructure.worker.binary.binary_stream_runner_bundle import BinaryStreamRunnerBundle
from scarajectory.infrastructure.worker.binary.ibinary_queue_drainer import IBinaryQueueDrainer
from scarajectory.infrastructure.worker.binary.ibinary_step_dispatcher import IBinaryStepDispatcher
from scarajectory.infrastructure.worker.binary.ibinary_stream_frame_handler import IBinaryStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
    def create(cls, bundle: BinaryStreamRunnerBundle) -> BinaryStreamLoopRunner:
        '''
            Constructs BinaryStreamLoopRunner with internal frame parser.

            :param bundle: BinaryStreamRunnerBundle containing collaborators.
            :return: BinaryStreamLoopRunner instance.
            :exceptions: None.
        '''
        step_bundle: BinaryStepBundle = BinaryStepBundle(
            flow_pacing=bundle.pacing_bundle.pacing_controller,
            packet_strategy=bundle.packet_strategy,
            byte_sender=bundle.byte_sender,
            state_controller=bundle.state_controller,
            observer_dispatcher=bundle.observer_dispatcher,
        )
        step_dispatcher: IBinaryStepDispatcher = (
            BinaryStepDispatcherFactory.create(step_bundle)
        )
        queue_drainer: IBinaryQueueDrainer = BinaryQueueDrainerFactory.create(
            state_controller=bundle.state_controller,
            observer_dispatcher=bundle.observer_dispatcher,
            pacing_config=bundle.pacing_config,
        )
        frame_handler: IBinaryStreamFrameHandler = (
            BinaryStreamFrameHandlerFactory.create(
                flow_pacing=bundle.pacing_bundle.pacing_controller,
                state_controller=bundle.state_controller,
                observer_dispatcher=bundle.observer_dispatcher,
            )
        )
        loop_bundle: BinaryLoopRunnerBundle = BinaryLoopRunnerBundle(
            step_dispatcher=step_dispatcher,
            queue_drainer=queue_drainer,
            frame_parser=BinaryFrameParserFactory.create(),
            frame_handler=frame_handler,
            pacing_config=bundle.pacing_config,
        )
        return BinaryStreamLoopRunner(loop_bundle)

    @classmethod
    def create_with_parser(
        cls,
        bundle: BinaryStreamRunnerBundle,
        frame_parser: IBinaryFrameParser,
    ) -> BinaryStreamLoopRunner:
        '''
            Constructs BinaryStreamLoopRunner with injected frame parser.

            :param bundle: BinaryStreamRunnerBundle containing collaborators.
            :param frame_parser: IBinaryFrameParser decoding inbound frames.
            :return: BinaryStreamLoopRunner instance.
            :exceptions: None.
        '''
        step_bundle: BinaryStepBundle = BinaryStepBundle(
            flow_pacing=bundle.pacing_bundle.pacing_controller,
            packet_strategy=bundle.packet_strategy,
            byte_sender=bundle.byte_sender,
            state_controller=bundle.state_controller,
            observer_dispatcher=bundle.observer_dispatcher,
        )
        step_dispatcher: IBinaryStepDispatcher = (
            BinaryStepDispatcherFactory.create(step_bundle)
        )
        queue_drainer: IBinaryQueueDrainer = BinaryQueueDrainerFactory.create(
            state_controller=bundle.state_controller,
            observer_dispatcher=bundle.observer_dispatcher,
            pacing_config=bundle.pacing_config,
        )
        frame_handler: IBinaryStreamFrameHandler = (
            BinaryStreamFrameHandlerFactory.create(
                flow_pacing=bundle.pacing_bundle.pacing_controller,
                state_controller=bundle.state_controller,
                observer_dispatcher=bundle.observer_dispatcher,
            )
        )
        loop_bundle: BinaryLoopRunnerBundle = BinaryLoopRunnerBundle(
            step_dispatcher=step_dispatcher,
            queue_drainer=queue_drainer,
            frame_parser=frame_parser,
            frame_handler=frame_handler,
            pacing_config=bundle.pacing_config,
        )
        return BinaryStreamLoopRunner(loop_bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
