# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory constructing StreamLoopRunner instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.worker.dispatcher.bundle import StepBundle
from scarajectory.infrastructure.worker.dispatcher.factory import StepDispatcherFactory
from scarajectory.infrastructure.worker.dispatcher.idispatcher import IStepDispatcher
from scarajectory.infrastructure.worker.drainer.dependencies import QueueDrainerDependencies
from scarajectory.infrastructure.worker.drainer.factory import QueueDrainerFactory
from scarajectory.infrastructure.worker.drainer.idrainer import IQueueDrainer
from scarajectory.infrastructure.worker.handler.dependencies import FrameHandlerDependencies
from scarajectory.infrastructure.worker.handler.factory import StreamFrameHandlerFactory
from scarajectory.infrastructure.worker.handler.ihandler import IStreamFrameHandler
from scarajectory.infrastructure.worker.runner.bundle import RunnerBundle
from scarajectory.infrastructure.worker.runner.loop_bundle import LoopRunnerBundle
from scarajectory.infrastructure.worker.runner.runner import StreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLoopRunnerFactory:
    '''
        Factory constructing StreamLoopRunner instances.

        It defines:

            :methods:
                | create - Constructs StreamLoopRunner from runner bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, bundle: RunnerBundle) -> StreamLoopRunner:
        '''
            Constructs StreamLoopRunner with runner bundle collaborators.

            :param bundle: RunnerBundle containing collaborators.
            :return: StreamLoopRunner instance.
            :exceptions: None.
        '''
        step_bundle: StepBundle = StepBundle(
            flow_pacing=bundle.pacing_bundle.flow_pacing_controller,
            packet_strategy=bundle.packet_strategy,
            byte_sender=bundle.byte_sender,
            state_controller=bundle.state_controller,
            observer_dispatcher=bundle.observer_dispatcher,
        )
        step_dispatcher: IStepDispatcher = (
            StepDispatcherFactory.create(step_bundle)
        )
        drainer_dependencies: QueueDrainerDependencies = (
            QueueDrainerDependencies(
                state_controller=bundle.state_controller,
                observer_dispatcher=bundle.observer_dispatcher,
                pacing_config=bundle.pacing_config,
            )
        )
        queue_drainer: IQueueDrainer = QueueDrainerFactory.create(
            drainer_dependencies
        )
        handler_dependencies: FrameHandlerDependencies = (
            FrameHandlerDependencies(
                flow_pacing=bundle.pacing_bundle.flow_pacing_controller,
                state_controller=bundle.state_controller,
                observer_dispatcher=bundle.observer_dispatcher,
                response_unpacker=bundle.parser_bundle.response_unpacker,
            )
        )
        frame_handler: IStreamFrameHandler = StreamFrameHandlerFactory.create(
            handler_dependencies
        )
        loop_bundle: LoopRunnerBundle = LoopRunnerBundle(
            step_dispatcher=step_dispatcher,
            queue_drainer=queue_drainer,
            frame_parser=bundle.parser_bundle.frame_parser,
            frame_handler=frame_handler,
            pacing_config=bundle.pacing_config,
        )
        return StreamLoopRunner(loop_bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
