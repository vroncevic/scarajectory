# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_frame_handler.py
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
    Dispatches inbound binary response frames to flow pacing and log observers.
'''

from __future__ import annotations

from struct import unpack
from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.parser.binary_payload_unpacker import BinaryPayloadUnpacker
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.service.pacing.iflow_pacing_controller import IFlowPacingController
from scarajectory.core.service.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamFrameHandler:
    '''
        Dispatches inbound binary response frames to flow pacing and log observers.

        It defines:

            :attributes:
                | _flow_pacing - IFlowPacingController managing sliding window queue.
                | _state_controller - IStreamStateController tracking lifecycle status.
                | _observer_dispatcher - IStreamObserverDispatcher emitting telemetry.
            :methods:
                | __init__ - Initializes handler with injected collaborators.
                | can_handle - Checks if message ID is supported by frame handler.
                | handle_frame - Processes parsed BinaryFrame and updates session state.
    '''

    _flow_pacing: IFlowPacingController
    _state_controller: IStreamStateController
    _observer_dispatcher: IStreamObserverDispatcher

    def __init__(
        self,
        *,
        flow_pacing: IFlowPacingController,
        state_controller: IStreamStateController,
        observer_dispatcher: IStreamObserverDispatcher,
    ) -> None:
        '''
            Initializes frame handler with flow pacing controller and observers.

            :param flow_pacing: Injected IFlowPacingController instance.
            :param state_controller: Injected IStreamStateController instance.
            :param observer_dispatcher: Injected IStreamObserverDispatcher instance.
            :exceptions: None.
        '''
        self._flow_pacing: Final[IFlowPacingController] = flow_pacing
        self._state_controller: Final[IStreamStateController] = state_controller
        self._observer_dispatcher: Final[IStreamObserverDispatcher] = observer_dispatcher

    def can_handle(self, msg_id: int) -> bool:
        '''
            Checks whether inbound message ID is supported by frame handler.

            :param msg_id: Message ID byte integer.
            :return: True if supported, False otherwise.
            :exceptions: None.
        '''
        return msg_id in (
            MessageId.RESP_ACK,
            MessageId.RESP_NACK,
            MessageId.RESP_MOVE_EVENT,
            MessageId.RESP_FAULT_EVENT,
            MessageId.RESP_DIAGNOSTICS,
            MessageId.RESP_STATUS,
        )

    def handle_frame(self, frame: BinaryFrame, session: StreamSession) -> bool:
        '''
            Processes inbound frame, updates session, and checks if critical stop is required.

            :param frame: Decoded BinaryFrame from transport.
            :param session: Active StreamSession instance.
            :return: True if critical fault requires immediate stop, False otherwise.
            :exceptions: None.
        '''
        match frame.msg_id:
            case MessageId.RESP_ACK:
                _, q_count = BinaryPayloadUnpacker.unpack_ack(frame.payload)
                self._flow_pacing.handle_binary_ack(session, q_count)
            case MessageId.RESP_NACK:
                session.failed_count += 1
                if session.remote_queue_depth > 0:
                    session.remote_queue_depth -= 1
            case MessageId.RESP_MOVE_EVENT:
                event_type, _ = unpack('<BI', frame.payload[:5])
                self._flow_pacing.handle_binary_move_event(session, event_type)
            case MessageId.RESP_FAULT_EVENT:
                severity, fault_code, _ = unpack('<BBI', frame.payload[:6])
                self._observer_dispatcher.notify_log(
                    f'[FIRMWARE FAULT]: code={fault_code} severity={severity}',
                    False,
                )
                if severity >= 2:
                    self._state_controller.set_state(StreamState.STOPPED)
                    return True
            case MessageId.RESP_DIAGNOSTICS:
                uptime_ms = (
                    unpack('<I', frame.payload[52:56])[0]
                    if len(frame.payload) >= 56
                    else 0
                )
                self._observer_dispatcher.notify_log(
                    f'[FIRMWARE DIAG]: uptime={uptime_ms}ms',
                    False,
                )
            case MessageId.RESP_STATUS:
                sys_state = frame.payload[0] if frame.payload else 0
                self._observer_dispatcher.notify_log(
                    f'[FIRMWARE STATUS]: state={sys_state}',
                    False,
                )
            case _:
                pass

        return False
