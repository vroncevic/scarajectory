# -*- coding: UTF-8 -*-

'''
Module
    stream_step_dispatcher_test.py
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
    Unit tests for StreamStepDispatcher and StreamStepDispatcherFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.worker.istream_step_dispatcher import IStreamStepDispatcher
from scarajectory.infrastructure.worker.stream_step_dispatcher import StreamStepDispatcher
from scarajectory.infrastructure.worker.stream_step_dispatcher_factory \
    import (
        StreamStepDispatcherFactory
    )

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamStepDispatcher(TestCase):
    '''
        Test cases verifying single step dispatching operations.
    '''

    def setUp(self) -> None:
        self.mock_pacing = MagicMock()
        self.mock_barrier = MagicMock()
        pacing_bundle = FlowPacingBundle(
            pacing_controller=self.mock_pacing,
            barrier_coordinator=self.mock_barrier,
        )
        self.mock_formatter = MagicMock()
        self.mock_sender = MagicMock()
        self.mock_state = MagicMock()
        self.mock_observer = MagicMock()

        self.dispatcher: StreamStepDispatcher = (
            StreamStepDispatcherFactory.create(
                pacing_bundle=pacing_bundle,
                formatter=self.mock_formatter,
                command_sender=self.mock_sender,
                state_controller=self.mock_state,
                observer_dispatcher=self.mock_observer,
            )
        )

    def test_protocol_conformance(self) -> None:
        '''
            Verifies that dispatcher satisfies IStreamStepDispatcher.
        '''
        self.assertIsInstance(self.dispatcher, IStreamStepDispatcher)

    def test_can_dispatch_step_true(self) -> None:
        '''
            Tests can_dispatch_step when queue has space.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self.mock_pacing.can_send.return_value = True
        self.assertTrue(self.dispatcher.can_dispatch_step(session))

    def test_can_dispatch_step_at_end(self) -> None:
        '''
            Tests can_dispatch_step returns False when all sent.
        '''
        session = StreamSession(
            waypoints=[Waypoint(x=10.0, y=20.0, z=0.0, speed=50.0)],
            sent_count=1,
            done_count=0,
            failed_count=0,
            remote_queue_depth=1,
            start_time=0.0,
        )
        self.assertFalse(self.dispatcher.can_dispatch_step(session))

    def test_dispatch_motion_step(self) -> None:
        '''
            Tests dispatching standard motion waypoint.
        '''
        wp = Waypoint(x=15.0, y=25.0, z=5.0, speed=30.0)
        session = StreamSession(
            waypoints=[wp],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )
        self.mock_formatter.format_move.return_value = 'G1 X15 Y25 Z5 F1800'

        self.dispatcher.dispatch_step(session)

        self.mock_sender.send_raw_command.assert_called_once_with(
            'G1 X15 Y25 Z5 F1800'
        )
        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.remote_queue_depth, 1)
        self.mock_observer.notify_progress.assert_called_once()

    def test_dispatch_command_step(self) -> None:
        '''
            Tests dispatching raw command waypoint with barrier trigger.
        '''
        wp = Waypoint(
            x=0.0, y=0.0, z=0.0, speed=0.0, command='M104 S200'
        )
        session = StreamSession(
            waypoints=[wp],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

        self.dispatcher.dispatch_step(session)

        self.mock_sender.send_raw_command.assert_called_once_with('M104 S200')
        self.mock_barrier.set_barrier.assert_called_once()
        self.assertEqual(session.sent_count, 1)
        self.assertEqual(session.remote_queue_depth, 0)


if __name__ == '__main__':
    main()
