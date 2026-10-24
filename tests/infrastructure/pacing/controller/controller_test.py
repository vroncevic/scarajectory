# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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

from scaracom.flow.barrier.barrier import FlowBarrier

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.infrastructure.pacing.controller.controller import FlowPacingController
from scarajectory.infrastructure.pacing.controller.dependencies import ControllerDependencies
from scarajectory.infrastructure.pacing.coordinator.coordinator import FlowBarrierCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class FlowPacingControllerTestCase(TestCase):
    '''Unit tests validating FlowPacingController behavior.'''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self._barrier = FlowBarrier()
        self._coordinator = FlowBarrierCoordinator(flow_barrier=self._barrier)

    def test_can_send_pacing(self) -> None:
        '''
            Verifies queue capacity and barrier throttling behavior in can_send.

            :exceptions: None.
        '''
        deps = ControllerDependencies(
            flow_barrier_coordinator=self._coordinator,
            capacity=2,
        )
        controller = FlowPacingController(deps)
        session = StreamSession(
            waypoints=[],
            sent_count=0,
            done_count=0,
            failed_count=0,
            remote_queue_depth=0,
            start_time=0.0,
        )

        self.assertTrue(controller.can_send(session))

        self._coordinator.set_barrier()
        self.assertFalse(controller.can_send(session))
        self._coordinator.clear_barrier()

        session.remote_queue_depth = 2
        self.assertFalse(controller.can_send(session))

        session.remote_queue_depth = 1
        self.assertFalse(controller.can_send(session, is_command=True))
        self.assertTrue(controller.can_send(session, is_command=False))

    def test_binary_ack_and_move_events(self) -> None:
        '''
            Verifies binary ACK free slots updating and move event progress handling.

            :exceptions: None.
        '''
        deps = ControllerDependencies(
            flow_barrier_coordinator=self._coordinator,
            capacity=10,
        )
        controller = FlowPacingController(deps)
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
