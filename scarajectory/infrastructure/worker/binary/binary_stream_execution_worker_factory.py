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

from scaralang.core.service.protocol.ibinary_frame_parser import IBinaryFrameParser

from scarajectory.infrastructure.worker.binary.binary_stream_execution_worker import BinaryStreamExecutionWorker
from scarajectory.infrastructure.worker.binary.binary_stream_loop_runner_factory import BinaryStreamLoopRunnerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_runner_bundle import BinaryStreamRunnerBundle
from scarajectory.infrastructure.worker.binary.ibinary_stream_loop_runner import IBinaryStreamLoopRunner
from scarajectory.infrastructure.worker.thread.iworker_thread_coordinator import IWorkerThreadCoordinator
from scarajectory.infrastructure.worker.thread.worker_thread_coordinator_factory import WorkerThreadCoordinatorFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
    def create(cls, bundle: BinaryStreamRunnerBundle) -> BinaryStreamExecutionWorker:
        '''
            Constructs BinaryStreamExecutionWorker with internal frame parser.

            :param bundle: BinaryStreamRunnerBundle containing worker dependencies.
            :return: BinaryStreamExecutionWorker instance.
            :exceptions: None.
        '''
        loop_runner: IBinaryStreamLoopRunner = BinaryStreamLoopRunnerFactory.create(bundle)
        coordinator: IWorkerThreadCoordinator = (
            WorkerThreadCoordinatorFactory.create(
                barrier_coordinator=bundle.pacing_bundle.barrier_coordinator
            )
        )

        return BinaryStreamExecutionWorker(
            loop_runner=loop_runner,
            coordinator=coordinator,
        )

    @classmethod
    def create_with_parser(
        cls,
        bundle: BinaryStreamRunnerBundle,
        frame_parser: IBinaryFrameParser,
    ) -> BinaryStreamExecutionWorker:
        '''
            Constructs BinaryStreamExecutionWorker with injected frame parser.

            :param bundle: BinaryStreamRunnerBundle containing worker dependencies.
            :param frame_parser: IBinaryFrameParser instance.
            :return: BinaryStreamExecutionWorker instance.
            :exceptions: None.
        '''
        loop_runner: IBinaryStreamLoopRunner = (
            BinaryStreamLoopRunnerFactory.create_with_parser(bundle, frame_parser)
        )
        coordinator: IWorkerThreadCoordinator = (
            WorkerThreadCoordinatorFactory.create(
                barrier_coordinator=bundle.pacing_bundle.barrier_coordinator
            )
        )

        return BinaryStreamExecutionWorker(
            loop_runner=loop_runner,
            coordinator=coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
