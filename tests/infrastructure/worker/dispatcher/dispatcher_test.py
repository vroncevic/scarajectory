# -*- coding: UTF-8 -*-

'''
Module
    dispatcher_test.py
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
    Unit tests for StepDispatcher implementation.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ibyte_sender import IByteSender
from scaralang.core.model.dsl.binary.step import BinaryStep

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.pacing.controller.icontroller import IFlowPacingController
from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.dispatcher.bundle import StepBundle
from scarajectory.infrastructure.worker.dispatcher.dispatcher import StepDispatcher
from scarajectory.infrastructure.worker.dispatcher.idispatcher import IStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StepDispatcherTestCase(TestCase):
    '''
        Unit tests for StepDispatcher.

        It defines:

            :methods:
                | setUp - Prepares test instance and mock collaborators.
                | test_structural_conformance - Verifies conformance to IStepDispatcher.
                | test_can_dispatch_step - Verifies delegation to flow pacing.
                | test_dispatch_waypoint - Verifies waypoint packet format and transmission.
                | test_dispatch_binary_step - Verifies pre-compiled step transmission.
    '''

    def setUp(self) -> None:
        '''
            Prepares dispatcher and mock collaborators.

            :exceptions: None.
        '''
        self.mock_flow = MagicMock(spec=IFlowPacingController)
        self.mock_strategy = MagicMock(spec=IPacketStrategy)
        self.mock_sender = MagicMock(spec=IByteSender)
        self.mock_state = MagicMock(spec=IStreamStateMachine)
        self.mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)

        bundle = StepBundle(
            flow_pacing=self.mock_flow,
            packet_strategy=self.mock_strategy,
            byte_sender=self.mock_sender,
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_dispatcher,
        )
        self.dispatcher = StepDispatcher(bundle)

    def test_structural_conformance(self) -> None:
        '''
            Verifies dispatcher satisfies IStepDispatcher structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.dispatcher, IStepDispatcher)

    def test_can_dispatch_step(self) -> None:
        '''
            Verifies can_dispatch_step delegates to flow pacing controller.

            :exceptions: None.
        '''
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.mock_flow.can_send.return_value = True
        self.assertTrue(self.dispatcher.can_dispatch_step(session))
        self.mock_flow.can_send.assert_called_once_with(session)

    def test_dispatch_waypoint(self) -> None:
        '''
            Verifies waypoint serialization, transmission, and counters increment.

            :exceptions: None.
        '''
        wp = TrajectoryWaypoint(
            x=10.0,
            y=20.0,
            z=30.0,
            phi=0.0,
            speed=50.0,
            name='P1',
            command='G1 X10 Y20 Z30',
        )
        session = StreamSession(
            waypoints=[wp],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )
        self.mock_strategy.format_waypoint_packet.return_value = b'\x01\x02\x03'

        self.dispatcher.dispatch_waypoint(session)

        self.mock_sender.send_raw_bytes.assert_called_once_with(b'\x01\x02\x03')
        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.remote_queue_depth, 1)
        self.mock_dispatcher.notify_progress.assert_called_once()

    def test_dispatch_binary_step(self) -> None:
        '''
            Verifies raw bytes dispatch for pre-compiled binary step.

            :exceptions: None.
        '''
        step = MagicMock(spec=BinaryStep)
        step.raw_bytes = b'\xAA\xBB\xCC'
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=100.0,
        )

        self.dispatcher.dispatch_binary_step(session=session, step=step)

        self.mock_sender.send_raw_bytes.assert_called_once_with(b'\xAA\xBB\xCC')
        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.remote_queue_depth, 1)
        self.mock_dispatcher.notify_progress.assert_called_once()


if __name__ == '__main__':
    main()
