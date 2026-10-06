# -*- coding: UTF-8 -*-

'''
Module
    binary_program_streamer_factory.py
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
    Defines factory for creating BinaryProgramStreamer instances.
'''

from __future__ import annotations

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.connection.iconnection import IConnection
from scarajectory.infrastructure.state.istream_state_machine import IStreamStateMachine
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.streaming.binary_program_streamer import BinaryProgramStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryProgramStreamerFactory:
    '''
        Factory providing creation of BinaryProgramStreamer instances.

        It defines:

            :methods:
                | create - Instantiates configured BinaryProgramStreamer.
                | get_version - Returns factory version string.
    '''

    def create(
        self,
        *,
        connection: IConnection,
        state_machine: IStreamStateMachine,
        dispatcher: IStreamObserverDispatcher,
        worker: IExecutionWorker,
        session: StreamSession,
    ) -> BinaryProgramStreamer:
        '''
            Instantiates configured BinaryProgramStreamer.

            :param connection: Injected IConnection instance.
            :param state_machine: Injected IStreamStateMachine instance.
            :param dispatcher: Injected IStreamObserverDispatcher instance.
            :param worker: Injected IExecutionWorker instance.
            :param session: Injected StreamSession instance.
            :return: Fully configured BinaryProgramStreamer.
        '''
        return BinaryProgramStreamer(
            connection=connection,
            state_machine=state_machine,
            dispatcher=dispatcher,
            worker=worker,
            session=session,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string representation.
        '''
        return __version__
