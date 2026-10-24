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
    Subsystem factory constructing worker services and adapters.
'''

from __future__ import annotations

from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.worker.dependencies import WorkerDependencies
from scarajectory.infrastructure.worker.execution.dependencies import ExecutionWorkerDependencies
from scarajectory.infrastructure.worker.execution.factory import StreamExecutionWorkerFactory
from scarajectory.infrastructure.worker.execution.worker import StreamExecutionWorker
from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.provides import WorkerProvides
from scarajectory.infrastructure.worker.receiver.dependencies import BytesReceiverDependencies
from scarajectory.infrastructure.worker.receiver.factory import StreamBytesReceiverFactory
from scarajectory.infrastructure.worker.receiver.receiver import StreamBytesReceiver
from scarajectory.infrastructure.worker.runner.bundle import RunnerBundle
from scarajectory.infrastructure.worker.runner.factory import StreamLoopRunnerFactory
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner
from scarajectory.infrastructure.worker.thread.factory import WorkerThreadCoordinatorFactory
from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerFactory:
    '''
        Subsystem factory constructing worker services and adapters.

        It defines:

            :methods:
                | create - Constructs WorkerProvides with execution worker and bytes receiver.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: WorkerDependencies) -> WorkerProvides:
        '''
            Constructs worker subsystem components wired together.

            :param dependencies: Injected WorkerDependencies container.
            :return: WorkerProvides containing execution worker and bytes receiver.
            :exceptions: None.
        '''
        runner_bundle = RunnerBundle(
            pacing_bundle=dependencies.pacing_bundle,
            packet_strategy=dependencies.packet_strategy,
            byte_sender=dependencies.byte_sender,
            state_controller=dependencies.state_controller,
            observer_dispatcher=dependencies.observer_dispatcher,
            pacing_config=dependencies.pacing_config,
            parser_bundle=dependencies.parser_bundle,
        )
        loop_runner: IStreamLoopRunner = StreamLoopRunnerFactory.create(runner_bundle)
        coordinator: IWorkerThreadCoordinator = WorkerThreadCoordinatorFactory.create(
            barrier_coordinator=dependencies.pacing_bundle.flow_barrier_coordinator
        )
        session_holder: StreamSessionHolder = StreamSessionHolder(
            session=SessionFactory.create_default()
        )
        exec_dependencies: ExecutionWorkerDependencies = (
            ExecutionWorkerDependencies(
                loop_runner=loop_runner,
                coordinator=coordinator,
                session_holder=session_holder,
            )
        )
        worker: StreamExecutionWorker = StreamExecutionWorkerFactory.create(
            exec_dependencies
        )
        rx_dependencies: BytesReceiverDependencies = BytesReceiverDependencies(
            loop_runner=loop_runner,
            worker=worker,
            session_holder=session_holder,
        )
        receiver: StreamBytesReceiver = StreamBytesReceiverFactory.create(
            rx_dependencies
        )
        return WorkerProvides(
            execution_worker=worker,
            bytes_receiver=receiver,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
