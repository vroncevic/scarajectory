# -*- coding: UTF-8 -*-

'''
Module
    stream_execution_worker_factory.py
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
    Factory service constructing StreamExecutionWorker background workers.
'''

from __future__ import annotations

from collections.abc import Callable

from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.core.service.communication.protocol.icommand_formatter import ICommandFormatter
from scarajectory.infrastructure.communication.protocol.ascii.formatter.command_formatter_factory import CommandFormatterFactory
from scarajectory.infrastructure.communication.streamer.flow_controller import FlowController
from scarajectory.infrastructure.communication.streamer.stream_execution_worker import StreamExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamExecutionWorkerFactory:
    '''
        Factory providing creation of StreamExecutionWorker instances.

        It defines:

            :methods:
                | create - Constructs StreamExecutionWorker with internal default formatter.
                | create_with_formatter - Constructs StreamExecutionWorker with explicit formatter.
    '''

    @classmethod
    def create(
        cls,
        *,
        flow_controller: FlowController,
        send_command: Callable[[str], bool],
        notify_progress: Callable[[str], None],
        notify_log: Callable[[str, bool], None],
        on_state_change: Callable[[StreamState], None],
        send_delay: float = 0.01,
        throttle_delay: float = 0.02,
        poll_delay: float = 0.05,
    ) -> StreamExecutionWorker:
        '''
            Constructs and returns a configured StreamExecutionWorker instance.

            :param flow_controller: FlowController instance.
            :param send_command: Callable transmitting raw command string.
            :param notify_progress: Callable emitting progress notifications.
            :param notify_log: Callable logging communication messages.
            :param on_state_change: Callable updating streamer state enum.
            :param send_delay: Pacing delay after transmit in seconds (default 0.01).
            :param throttle_delay: Throttle backoff delay in seconds (default 0.02).
            :param poll_delay: Polling interval in seconds (default 0.05).
            :return: StreamExecutionWorker instance.
        '''
        formatter: ICommandFormatter = CommandFormatterFactory.create()

        return StreamExecutionWorker(
            flow_controller=flow_controller,
            formatter=formatter,
            send_command=send_command,
            notify_progress=notify_progress,
            notify_log=notify_log,
            on_state_change=on_state_change,
            send_delay=send_delay,
            throttle_delay=throttle_delay,
            poll_delay=poll_delay,
        )

    @classmethod
    def create_with_formatter(
        cls,
        *,
        flow_controller: FlowController,
        formatter: ICommandFormatter,
        send_command: Callable[[str], bool],
        notify_progress: Callable[[str], None],
        notify_log: Callable[[str, bool], None],
        on_state_change: Callable[[StreamState], None],
        send_delay: float = 0.01,
        throttle_delay: float = 0.02,
        poll_delay: float = 0.05,
    ) -> StreamExecutionWorker:
        '''
            Constructs and returns a configured StreamExecutionWorker with injected formatter.

            :param flow_controller: FlowController instance.
            :param formatter: ICommandFormatter instance.
            :param send_command: Callable transmitting raw command string.
            :param notify_progress: Callable emitting progress notifications.
            :param notify_log: Callable logging communication messages.
            :param on_state_change: Callable updating streamer state enum.
            :param send_delay: Pacing delay after transmit in seconds (default 0.01).
            :param throttle_delay: Throttle backoff delay in seconds (default 0.02).
            :param poll_delay: Polling interval in seconds (default 0.05).
            :return: StreamExecutionWorker instance.
        '''
        return StreamExecutionWorker(
            flow_controller=flow_controller,
            formatter=formatter,
            send_command=send_command,
            notify_progress=notify_progress,
            notify_log=notify_log,
            on_state_change=on_state_change,
            send_delay=send_delay,
            throttle_delay=throttle_delay,
            poll_delay=poll_delay,
        )

