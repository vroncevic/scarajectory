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
    Unit testing for PlaybackController.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.streaming.control.itransmitter import IControlTransmitter
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.pacing.coordinator.icoordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.streaming.playback.controller import PlaybackController
from scarajectory.infrastructure.streaming.playback.dependencies import PlaybackDependencies
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlaybackController(TestCase):
    '''
    Test cases verifying PlaybackController lifecycle and execution controls.

    It defines:

        :methods:
            | setUp - Prepares mock collaborators and PlaybackController instance.
            | test_satisfies_protocol - Verifies IPlaybackController structural contract.
            | test_start_streaming_disconnected - Verifies start_streaming fails when offline.
            | test_start_streaming_empty_waypoints - Verifies start_streaming fails when list is empty.
            | test_start_streaming_success - Verifies start_streaming transitions state and starts worker.
            | test_pause_streaming - Verifies pause_streaming transitions state and sends hold.
            | test_resume_streaming - Verifies resume_streaming transitions state and sends resume.
            | test_stop_streaming - Verifies stop_streaming stops worker and sends estop.
    '''

    def setUp(self) -> None:
        '''
        Prepares mock collaborators and PlaybackController instance.

        :exceptions: None.
        '''
        self.connection_manager = MagicMock(spec=IConnectionManager)
        self.barrier_coordinator = MagicMock(spec=IFlowBarrierCoordinator)
        self.state_machine = MagicMock(spec=IStreamStateMachine)
        self.dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.worker = MagicMock(spec=IExecutionWorker)
        self.transmitter = MagicMock(spec=IControlTransmitter)
        deps = PlaybackDependencies(
            connection_manager=self.connection_manager,
            flow_barrier_coordinator=self.barrier_coordinator,
            stream_state_machine=self.state_machine,
            stream_observer_dispatcher=self.dispatcher,
            execution_worker=self.worker,
            control_transmitter=self.transmitter,
        )
        self.controller = PlaybackController(dependencies=deps)

    def test_satisfies_protocol(self) -> None:
        '''
            Verifies IPlaybackController structural contract.

            :exceptions: None.
        '''
        self.assertIsInstance(self.controller, IPlaybackController)

    def test_start_streaming_disconnected(self) -> None:
        '''
            Verifies start_streaming fails when offline.

            :exceptions: None.
        '''
        self.connection_manager.is_connected.return_value = False
        waypoint = TrajectoryWaypoint(x=1.0, y=2.0, z=3.0, speed=10.0, phi=0.0, name='', command='')
        result: bool = self.controller.start_streaming([waypoint])
        self.assertFalse(result)
        self.dispatcher.notify_log.assert_called_with(
            '[ERR]: Cannot stream - Transport not connected'
        )

    def test_start_streaming_empty_waypoints(self) -> None:
        '''
            Verifies start_streaming fails when list is empty.

            :exceptions: None.
        '''
        self.connection_manager.is_connected.return_value = True
        result: bool = self.controller.start_streaming([])
        self.assertFalse(result)

    def test_start_streaming_success(self) -> None:
        '''
            Verifies start_streaming transitions state and starts worker.

            :exceptions: None.
        '''
        self.connection_manager.is_connected.return_value = True
        waypoint = TrajectoryWaypoint(x=-23.0, y=-88.0, z=3.0, speed=10.0, phi=0.0, name='', command='')
        result: bool = self.controller.start_streaming([waypoint])
        self.assertTrue(result)
        self.state_machine.transition_to.assert_called_with(
            StreamState.STREAMING
        )
        self.worker.start_waypoints.assert_called_once()
        self.transmitter.send_enable.assert_called_once()
        warning_logged: bool = any(
            'requires Lefty elbow configuration' in str(call_arg)
            for call_arg in self.dispatcher.notify_log.call_args_list
        )
        self.assertTrue(warning_logged)

    def test_pause_streaming(self) -> None:
        '''
            Verifies pause_streaming transitions state and sends hold.

            :exceptions: None.
        '''
        self.state_machine.state = StreamState.STREAMING
        self.state_machine.is_active.return_value = True
        self.connection_manager.is_connected.return_value = True
        self.controller.pause_streaming()
        self.state_machine.transition_to.assert_called_with(
            StreamState.PAUSED
        )
        self.worker.set_paused.assert_called_once_with(True)
        self.transmitter.send_hold.assert_called_once()

    def test_resume_streaming(self) -> None:
        '''
            Verifies resume_streaming transitions state and sends resume.

            :exceptions: None.
        '''
        self.state_machine.state = StreamState.PAUSED
        self.state_machine.is_active.return_value = True
        self.connection_manager.is_connected.return_value = True
        self.controller.resume_streaming()
        self.state_machine.transition_to.assert_called_with(
            StreamState.STREAMING
        )
        self.worker.set_paused.assert_called_once_with(False)
        self.transmitter.send_resume.assert_called_once()

    def test_stop_streaming(self) -> None:
        '''
            Verifies stop_streaming stops worker and sends estop.

            :exceptions: None.
        '''
        self.state_machine.is_active.return_value = True
        self.connection_manager.is_connected.return_value = True
        self.controller.stop_streaming()
        self.state_machine.transition_to.assert_called_with(
            StreamState.STOPPED
        )
        self.worker.stop.assert_called_once()
        self.transmitter.send_estop.assert_called_once()


if __name__ == '__main__':
    main()
