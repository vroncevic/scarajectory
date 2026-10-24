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
    Unit tests for StepDispatcherFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ibyte_sender import IByteSender

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.pacing.controller.icontroller import IFlowPacingController
from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.dispatcher.bundle import StepBundle
from scarajectory.infrastructure.worker.dispatcher.dispatcher import StepDispatcher
from scarajectory.infrastructure.worker.dispatcher.factory import StepDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepDispatcherFactoryTestCase(TestCase):
    '''
        Unit tests for StepDispatcherFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creates StepDispatcher instance.
                | test_version - Verifies factory get_version returns string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates StepDispatcher instance.

            :exceptions: None.
        '''
        mock_flow = MagicMock(spec=IFlowPacingController)
        mock_strategy = MagicMock(spec=IPacketStrategy)
        mock_sender = MagicMock(spec=IByteSender)
        mock_state = MagicMock(spec=IStreamStateMachine)
        mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)

        bundle = StepBundle(
            flow_pacing=mock_flow,
            packet_strategy=mock_strategy,
            byte_sender=mock_sender,
            state_controller=mock_state,
            observer_dispatcher=mock_dispatcher,
        )

        dispatcher = StepDispatcherFactory.create(bundle)
        self.assertIsInstance(dispatcher, StepDispatcher)

    def test_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(StepDispatcherFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
