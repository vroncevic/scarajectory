# -*- coding: UTF-8 -*-

'''
Module
    flow_pacing_controller_test.py
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
    Unit tests for FlowPacingController component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.pacing.iflow_pacing_controller import (
    IFlowPacingController,
)
from scarajectory.infrastructure.barrier.flow_barrier_factory import (
    FlowBarrierFactory,
)
from scarajectory.infrastructure.pacing.flow_barrier_coordinator_factory import (
    FlowBarrierCoordinatorFactory,
)
from scarajectory.infrastructure.pacing.flow_pacing_controller_factory import (
    FlowPacingControllerFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestFlowPacingController(TestCase):
    '''
        Test cases for FlowPacingController component.

        It defines:

            :methods:
                | test_flow_pacing_controller_protocol - Verifies protocol conformance.
                | test_can_send_pacing - Verifies queue capacity and barrier throttling.
                | test_process_response_handling - Verifies response lines and error dispatching.
                | test_binary_ack_and_move_events - Verifies binary ACK and move event handling.
    '''

    def test_flow_pacing_controller_protocol(self) -> None:
        '''
            Verifies that FlowPacingController satisfies IFlowPacingController.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        controller = FlowPacingControllerFactory.create(
            barrier_coordinator=coordinator,
            capacity=16,
        )
        self.assertIsInstance(controller, IFlowPacingController)

    def test_can_send_pacing(self) -> None:
        '''
            Verifies queue capacity and barrier throttling behavior in can_send.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        controller = FlowPacingControllerFactory.create(
            barrier_coordinator=coordinator,
            capacity=2,
        )
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

        self.assertTrue(controller.can_send(session))

        coordinator.set_barrier()
        self.assertFalse(controller.can_send(session))
        coordinator.clear_barrier()

        session.remote_queue_depth = 2
        self.assertFalse(controller.can_send(session))

        session.remote_queue_depth = 1
        self.assertFalse(controller.can_send(session, is_command=True))
        self.assertTrue(controller.can_send(session, is_command=False))

    def test_process_response_handling(self) -> None:
        '''
            Verifies response processing for homing failure, moves, and buffer metrics.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        controller = FlowPacingControllerFactory.create(
            barrier_coordinator=coordinator,
            capacity=8,
        )
        session = StreamSession(
            waypoints=[
                Waypoint(x=10.0, y=10.0, z=0.0, speed=50.0),
                Waypoint(x=20.0, y=20.0, z=0.0, speed=50.0),
            ],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=3,
            start_time=0.0,
        )

        fatal, msg = controller.process_response('HOMING_FAILED', session)
        self.assertTrue(fatal)
        self.assertIn('Homing Failed', msg)
        self.assertTrue(coordinator.is_barrier_clear())

        coordinator.set_barrier()
        fatal, msg = controller.process_response('WAIT_DONE', session)
        self.assertFalse(fatal)
        self.assertTrue(coordinator.is_barrier_clear())

        fatal, msg = controller.process_response('<RESP:ACK#1:QUEUE=5>', session)
        self.assertFalse(fatal)
        self.assertEqual(session.remote_queue_depth, 5)

        fatal, msg = controller.process_response(
            '<RESP:BUFFER_FULL#Q:8>', session
        )
        self.assertFalse(fatal)
        self.assertEqual(session.remote_queue_depth, 8)

        fatal, msg = controller.process_response('<RESP:OK#MOVE:1>', session)
        self.assertFalse(fatal)
        self.assertEqual(session.done_count, 1)

        coordinator.set_barrier()
        fatal, msg = controller.process_response('<RESP:MOVE_FAILED#1>', session)
        self.assertFalse(fatal)
        self.assertTrue(coordinator.is_barrier_clear())
        self.assertEqual(session.failed_count, 2)

        coordinator.set_barrier()
        fatal, msg = controller.process_response('<RESP:ERR#SYNTAX>', session)
        self.assertFalse(fatal)
        self.assertTrue(coordinator.is_barrier_clear())

        fatal, msg = controller.process_response('PLAIN_TEXT_IGNORE', session)
        self.assertFalse(fatal)
        self.assertEqual(msg, '')

    def test_binary_ack_and_move_events(self) -> None:
        '''
            Verifies binary ACK free slots updating and move event progress handling.
        '''
        barrier = FlowBarrierFactory.create()
        coordinator = FlowBarrierCoordinatorFactory.create(barrier)
        controller = FlowPacingControllerFactory.create(
            barrier_coordinator=coordinator,
            capacity=10,
        )
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=10,
            start_time=0.0,
        )

        controller.handle_binary_ack(session, free_slots=6)
        self.assertEqual(session.remote_queue_depth, 4)

        controller.handle_binary_move_event(session, event_type=2)
        self.assertEqual(session.done_count, 1)
        self.assertEqual(session.remote_queue_depth, 3)

        controller.handle_binary_move_event(session, event_type=3)
        self.assertEqual(session.failed_count, 1)
        self.assertEqual(session.remote_queue_depth, 2)

        controller.handle_binary_move_event(session, event_type=1)
        self.assertEqual(session.done_count, 1)


if __name__ == '__main__':
    main()
