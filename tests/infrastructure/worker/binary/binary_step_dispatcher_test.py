# -*- coding: UTF-8 -*-

'''
Module
    binary_step_dispatcher_test.py
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
    Unit tests for BinaryStepDispatcher and its factory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.step import Step

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.worker.binary.binary_step_bundle import BinaryStepBundle
from scarajectory.infrastructure.worker.binary.binary_step_dispatcher import BinaryStepDispatcher
from scarajectory.infrastructure.worker.binary.binary_step_dispatcher_factory import BinaryStepDispatcherFactory
from scarajectory.infrastructure.worker.binary.ibinary_step_dispatcher import IBinaryStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStepDispatcherTestCase(TestCase):
    '''
        Tests BinaryStepDispatcher transmission of waypoints and binary steps.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and dispatcher.
                | test_factory_and_protocol - Tests construction and protocol adherence.
                | test_can_dispatch_step - Tests flow pacing check.
                | test_dispatch_waypoint - Tests waypoint packet formatting and transmission.
                | test_dispatch_binary_step - Tests raw step transmission.
    '''

    def setUp(self) -> None:
        self.mock_flow = MagicMock()
        self.mock_strategy = MagicMock()
        self.mock_sender = MagicMock()
        self.mock_state = MagicMock()
        self.mock_state.state = StreamState.STREAMING
        self.mock_observer = MagicMock()

        bundle = BinaryStepBundle(
            flow_pacing=self.mock_flow,
            packet_strategy=self.mock_strategy,
            byte_sender=self.mock_sender,
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_observer,
        )
        self.dispatcher: BinaryStepDispatcher = (
            BinaryStepDispatcherFactory.create(bundle)
        )

    def test_factory_and_protocol(self) -> None:
        '''Tests factory creation and protocol adherence.'''
        self.assertIsInstance(self.dispatcher, IBinaryStepDispatcher)
        version: str = BinaryStepDispatcherFactory.get_version()
        self.assertEqual(version, '1.0.3')

    def test_can_dispatch_step(self) -> None:
        '''Tests can_dispatch_step delegation to flow pacing.'''
        session: StreamSession = SessionFactory.create(waypoints=[])
        self.mock_flow.can_send.return_value = True
        self.assertTrue(self.dispatcher.can_dispatch_step(session))

        self.mock_flow.can_send.return_value = False
        self.assertFalse(self.dispatcher.can_dispatch_step(session))

    def test_dispatch_waypoint(self) -> None:
        '''Tests dispatching a waypoint updates counters and transmits bytes.'''
        waypoint = Waypoint(x=10.0, y=20.0, z=0.0, speed=5.0)
        session: StreamSession = SessionFactory.create(waypoints=[waypoint])
        self.mock_strategy.format_waypoint_packet.return_value = b'\x01\x02\x03'

        self.dispatcher.dispatch_waypoint(session)

        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.remote_queue_depth, 1)
        self.mock_sender.send_raw_bytes.assert_called_once_with(b'\x01\x02\x03')
        self.mock_observer.notify_progress.assert_called_once_with(
            state=StreamState.STREAMING,
            session=session,
            error='',
        )

    def test_dispatch_binary_step(self) -> None:
        '''Tests dispatching a pre-compiled binary step.'''
        session: StreamSession = SessionFactory.create(waypoints=[])
        mock_step = MagicMock(spec=Step)
        mock_step.raw_bytes = b'\xDE\xAD\xBE\xEF'

        self.dispatcher.dispatch_binary_step(session=session, step=mock_step)

        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.remote_queue_depth, 1)
        self.mock_sender.send_raw_bytes.assert_called_once_with(
            b'\xDE\xAD\xBE\xEF'
        )
        self.mock_observer.notify_progress.assert_called_once_with(
            state=StreamState.STREAMING,
            session=session,
            error='',
        )


if __name__ == '__main__':
    main()
