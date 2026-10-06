# -*- coding: UTF-8 -*-

'''
Module
    stream_playback_controller_factory.py
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
    Factory instantiating StreamPlaybackController instances.
'''

from __future__ import annotations

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.pacing.iflow_barrier_coordinator import IFlowBarrierCoordinator
from scarajectory.infrastructure.connection.iconnection import IConnection
from scarajectory.infrastructure.state.istream_state_machine import IStreamStateMachine
from scarajectory.core.service.streaming.istream_control_transmitter import IStreamControlTransmitter
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.streaming.stream_playback_controller import StreamPlaybackController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPlaybackControllerFactory:
    '''
        Factory instantiating StreamPlaybackController instances.

        It defines:

            :methods:
                | create - Constructs StreamPlaybackController instance with injected collaborators.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        connection: IConnection,
        barrier_coordinator: IFlowBarrierCoordinator,
        state_machine: IStreamStateMachine,
        dispatcher: IStreamObserverDispatcher,
        worker: IExecutionWorker,
        control_transmitter: IStreamControlTransmitter,
        session: StreamSession,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> StreamPlaybackController:
        '''
            Constructs StreamPlaybackController instance with injected collaborators.

            :param connection: Injected IConnection instance.
            :param barrier_coordinator: Injected IFlowBarrierCoordinator instance.
            :param state_machine: Injected IStreamStateMachine instance.
            :param dispatcher: Injected IStreamObserverDispatcher instance.
            :param worker: Injected IExecutionWorker instance.
            :param control_transmitter: Injected IStreamControlTransmitter instance.
            :param session: Injected StreamSession instance.
            :param protocol_mode: Active wire protocol mode enum value.
            :return: Fully wired StreamPlaybackController instance.
        '''
        return StreamPlaybackController(
            connection=connection,
            barrier_coordinator=barrier_coordinator,
            state_machine=state_machine,
            dispatcher=dispatcher,
            worker=worker,
            control_transmitter=control_transmitter,
            session=session,
            protocol_mode=protocol_mode,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
        '''
        return __version__
