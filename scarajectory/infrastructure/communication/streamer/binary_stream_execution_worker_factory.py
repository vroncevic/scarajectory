# -*- coding: UTF-8 -*-

"""
Module
    binary_stream_execution_worker_factory.py
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
    Factory constructing BinaryStreamExecutionWorker instances.
"""

from __future__ import annotations

from collections.abc import Callable

from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy import BinaryPacketStrategy
from scarajectory.infrastructure.communication.streamer.binary_stream_execution_worker import BinaryStreamExecutionWorker
from scarajectory.infrastructure.communication.streamer.flow_controller import FlowController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamExecutionWorkerFactory:
    """
        Factory constructing BinaryStreamExecutionWorker instances with configured callbacks.

        It defines:

            :methods:
                | create - Constructs BinaryStreamExecutionWorker with internal frame parser.
                | create_with_parser - Constructs BinaryStreamExecutionWorker with injected frame parser.
                | get_version - Returns factory version string.
    """

    @classmethod
    def create(
        cls,
        *,
        flow_controller: FlowController,
        packet_strategy: BinaryPacketStrategy,
        send_bytes: Callable[[bytes], bool],
        notify_progress: Callable[[str], None],
        notify_log: Callable[[str, bool], None],
        on_state_change: Callable[[StreamState], None],
        send_delay: float = 0.005,
        throttle_delay: float = 0.01,
        poll_delay: float = 0.02,
    ) -> BinaryStreamExecutionWorker:
        '''
            Constructs BinaryStreamExecutionWorker with internal frame parser.

            :param flow_controller: FlowController instance.
            :param packet_strategy: BinaryPacketStrategy instance.
            :param send_bytes: Transport byte transmission callback.
            :param notify_progress: Progress update callback.
            :param notify_log: Log update callback.
            :param on_state_change: State change callback.
            :param send_delay: Transmission delay in seconds.
            :param throttle_delay: Throttling delay in seconds.
            :param poll_delay: Polling delay in seconds.
            :return: BinaryStreamExecutionWorker instance.
        '''
        return BinaryStreamExecutionWorker(
            flow_controller=flow_controller,
            packet_strategy=packet_strategy,
            frame_parser=BinaryFrameParserFactory.create(),
            send_bytes=send_bytes,
            notify_progress=notify_progress,
            notify_log=notify_log,
            on_state_change=on_state_change,
            send_delay=send_delay,
            throttle_delay=throttle_delay,
            poll_delay=poll_delay,
        )

    @classmethod
    def create_with_parser(
        cls,
        *,
        flow_controller: FlowController,
        packet_strategy: BinaryPacketStrategy,
        frame_parser: BinaryFrameParser,
        send_bytes: Callable[[bytes], bool],
        notify_progress: Callable[[str], None],
        notify_log: Callable[[str, bool], None],
        on_state_change: Callable[[StreamState], None],
        send_delay: float = 0.005,
        throttle_delay: float = 0.01,
        poll_delay: float = 0.02,
    ) -> BinaryStreamExecutionWorker:
        '''
            Constructs BinaryStreamExecutionWorker with injected frame parser.

            :param flow_controller: FlowController instance.
            :param packet_strategy: BinaryPacketStrategy instance.
            :param frame_parser: BinaryFrameParser instance.
            :param send_bytes: Transport byte transmission callback.
            :param notify_progress: Progress update callback.
            :param notify_log: Log update callback.
            :param on_state_change: State change callback.
            :param send_delay: Transmission delay in seconds.
            :param throttle_delay: Throttling delay in seconds.
            :param poll_delay: Polling delay in seconds.
            :return: BinaryStreamExecutionWorker instance.
        '''
        return BinaryStreamExecutionWorker(
            flow_controller=flow_controller,
            packet_strategy=packet_strategy,
            frame_parser=frame_parser,
            send_bytes=send_bytes,
            notify_progress=notify_progress,
            notify_log=notify_log,
            on_state_change=on_state_change,
            send_delay=send_delay,
            throttle_delay=throttle_delay,
            poll_delay=poll_delay,
        )

    @classmethod
    def get_version(cls) -> str:
        return __version__


