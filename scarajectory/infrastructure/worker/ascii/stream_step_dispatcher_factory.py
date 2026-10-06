# -*- coding: UTF-8 -*-

'''
Module
    stream_step_dispatcher_factory.py
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
    Factory for instantiating StreamStepDispatcher components.
'''

from __future__ import annotations

from scarajectory.infrastructure.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.formatter.icommand_formatter import ICommandFormatter
from scarajectory.infrastructure.connection.icommand_sender import ICommandSender
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.worker.ascii.stream_step_dispatcher import StreamStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStepDispatcherFactory:
    '''
        Factory constructing StreamStepDispatcher instances.

        It defines:

            :methods:
                | create - Constructs and returns StreamStepDispatcher.
                | get_version - Returns factory module semantic version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        pacing_bundle: FlowPacingBundle,
        formatter: ICommandFormatter,
        command_sender: ICommandSender,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
    ) -> StreamStepDispatcher:
        '''
            Constructs and returns StreamStepDispatcher.

            :param pacing_bundle: FlowPacingBundle managing pacing and barrier.
            :param formatter: Formatter converting waypoints to commands.
            :param command_sender: Sender transmitting raw command strings.
            :param state_controller: Controller managing streaming state.
            :param observer_dispatcher: Dispatcher publishing telemetry.
            :return: Configured StreamStepDispatcher instance.
            :exceptions: None.
        '''
        return StreamStepDispatcher(
            pacing_bundle=pacing_bundle,
            formatter=formatter,
            command_sender=command_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__
