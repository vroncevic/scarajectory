# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit testing for PlaybackDependencies dataclass.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.control.itransmitter import IControlTransmitter
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.pacing.coordinator.icoordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.streaming.playback.dependencies import PlaybackDependencies
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlaybackDependencies(TestCase):
    '''
    Test cases verifying PlaybackDependencies parameter bundle.

    It defines:

        :methods:
            | test_initialization - Tests attributes.
    '''

    def test_initialization(self) -> None:
        '''
            Tests initialization and immutability of PlaybackDependencies.

            :exceptions: None.
        '''
        connection_manager = MagicMock(spec=IConnectionManager)
        barrier = MagicMock(spec=IFlowBarrierCoordinator)
        state_machine = MagicMock(spec=IStreamStateMachine)
        dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        worker = MagicMock(spec=IExecutionWorker)
        transmitter = MagicMock(spec=IControlTransmitter)
        deps = PlaybackDependencies(
            connection_manager=connection_manager,
            flow_barrier_coordinator=barrier,
            stream_state_machine=state_machine,
            stream_observer_dispatcher=dispatcher,
            execution_worker=worker,
            control_transmitter=transmitter,
        )

        self.assertIs(deps.connection_manager, connection_manager)
        self.assertIs(deps.flow_barrier_coordinator, barrier)
        self.assertIs(deps.stream_state_machine, state_machine)
        self.assertIs(deps.stream_observer_dispatcher, dispatcher)
        self.assertIs(deps.execution_worker, worker)
        self.assertIs(deps.control_transmitter, transmitter)


if __name__ == '__main__':
    main()
