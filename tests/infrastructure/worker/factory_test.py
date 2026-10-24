# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for WorkerFactory subsystem factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ibyte_sender import IByteSender

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.pacing.provides import PacingProvides
from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.dependencies import WorkerDependencies
from scarajectory.infrastructure.worker.factory import WorkerFactory
from scarajectory.infrastructure.worker.parser.bundle import ParserBundle
from scarajectory.infrastructure.worker.provides import WorkerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerFactoryTestCase(TestCase):
    '''
        Unit tests for WorkerFactory.

        It defines:

            :methods:
                | test_worker_factory_create - Verifies factory creates WorkerProvides.
                | test_worker_factory_version - Verifies factory get_version returns string.
    '''

    def test_worker_factory_create(self) -> None:
        '''
            Verifies factory creates configured WorkerProvides instance.

            :exceptions: None.
        '''
        mock_pacing = MagicMock(spec=PacingProvides)
        mock_strategy = MagicMock(spec=IPacketStrategy)
        mock_sender = MagicMock(spec=IByteSender)
        mock_state = MagicMock(spec=IStreamStateMachine)
        mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        mock_config = MagicMock(spec=StreamPacingConfig)
        mock_parser_bundle = MagicMock(spec=ParserBundle)

        deps = WorkerDependencies(
            pacing_bundle=mock_pacing,
            packet_strategy=mock_strategy,
            byte_sender=mock_sender,
            state_controller=mock_state,
            observer_dispatcher=mock_dispatcher,
            pacing_config=mock_config,
            parser_bundle=mock_parser_bundle,
        )

        provides: WorkerProvides = WorkerFactory.create(deps)
        self.assertIsInstance(provides, WorkerProvides)
        self.assertIsNotNone(provides.execution_worker)
        self.assertIsNotNone(provides.bytes_receiver)

    def test_worker_factory_version(self) -> None:
        '''
            Verifies factory get_version method returns valid string.

            :exceptions: None.
        '''
        self.assertEqual(WorkerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
