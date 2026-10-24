# -*- coding: UTF-8 -*-

'''
Module
    handler_test.py
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
    Unit tests for StreamFrameHandler implementation.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.protocol.iresponse_unpacker import IBinaryResponsePayloadUnpacker

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.core.model.streaming.state import StreamState
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.pacing.controller.icontroller import IFlowPacingController
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.handler.handler import StreamFrameHandler
from scarajectory.infrastructure.worker.handler.ihandler import IStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamFrameHandlerTestCase(TestCase):
    '''
        Unit tests for StreamFrameHandler.

        It defines:

            :methods:
                | setUp - Prepares handler and mock collaborators.
                | test_structural_conformance - Verifies conformance to IStreamFrameHandler.
                | test_can_handle - Verifies supported message IDs.
                | test_handle_ack - Verifies ACK frame handling.
                | test_handle_nack - Verifies NACK frame handling.
                | test_handle_fault - Verifies severe fault handling transitions to STOPPED.
    '''

    def setUp(self) -> None:
        '''
            Prepares test handler and mock collaborators.

            :exceptions: None.
        '''
        self.mock_flow = MagicMock(spec=IFlowPacingController)
        self.mock_state = MagicMock(spec=IStreamStateMachine)
        self.mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        self.mock_unpacker = MagicMock(spec=IBinaryResponsePayloadUnpacker)
        self.handler = StreamFrameHandler(
            flow_pacing=self.mock_flow,
            state_controller=self.mock_state,
            observer_dispatcher=self.mock_dispatcher,
            response_unpacker=self.mock_unpacker,
        )
        self.session = StreamSession(
            waypoints=[],
            sent_count=5,
            done_count=0,
            failed_count=0,
            remote_queue_depth=3,
            start_time=100.0,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies handler satisfies IStreamFrameHandler structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.handler, IStreamFrameHandler)

    def test_can_handle(self) -> None:
        '''
            Verifies supported message IDs.

            :exceptions: None.
        '''
        self.assertTrue(self.handler.can_handle(int(MessageId.RESP_ACK)))
        self.assertTrue(self.handler.can_handle(int(MessageId.RESP_NACK)))
        self.assertFalse(self.handler.can_handle(999))

    def test_handle_ack(self) -> None:
        '''
            Verifies ACK payload handling delegates to flow pacing.

            :exceptions: None.
        '''
        self.mock_unpacker.unpack_ack.return_value = (1, 2)
        frame = BinaryFrame(
            msg_id=int(MessageId.RESP_ACK),
            seq_num=1,
            payload=b'\x01\x02',
            crc16=0,
        )
        result = self.handler.handle_frame(frame, self.session)
        self.assertFalse(result)
        self.mock_flow.handle_binary_ack.assert_called_once_with(self.session, 2)

    def test_handle_nack(self) -> None:
        '''
            Verifies NACK frame updates session counters and emits log.

            :exceptions: None.
        '''
        self.mock_unpacker.unpack_nack.return_value = (1, 404)
        frame = BinaryFrame(
            msg_id=int(MessageId.RESP_NACK),
            seq_num=1,
            payload=b'\x01\x02',
            crc16=0,
        )
        result = self.handler.handle_frame(frame, self.session)
        self.assertFalse(result)
        self.assertEqual(self.session.failed_count, 1)
        self.assertEqual(self.session.remote_queue_depth, 2)
        self.mock_dispatcher.notify_log.assert_called_once()

    def test_handle_fault(self) -> None:
        '''
            Verifies critical fault frame returns True and transitions state.

            :exceptions: None.
        '''
        payload = pack('<BBI', 2, 55, 1000)
        frame = BinaryFrame(
            msg_id=int(MessageId.RESP_FAULT_EVENT),
            seq_num=1,
            payload=payload,
            crc16=0,
        )
        result = self.handler.handle_frame(frame, self.session)
        self.assertTrue(result)
        self.mock_state.transition_to.assert_called_once_with(StreamState.STOPPED)

        low_fault = BinaryFrame(
            msg_id=int(MessageId.RESP_FAULT_EVENT),
            seq_num=2,
            payload=pack('<BBI', 1, 12, 500),
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(low_fault, self.session))

        move_frame = BinaryFrame(
            msg_id=int(MessageId.RESP_MOVE_EVENT),
            seq_num=3,
            payload=pack('<BI', 3, 100),
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(move_frame, self.session))
        self.mock_flow.handle_binary_move_event.assert_called_once_with(self.session, 3)

        diag_payload = b'\x00' * 52 + pack('<I', 12345)
        diag_frame = BinaryFrame(
            msg_id=int(MessageId.RESP_DIAGNOSTICS),
            seq_num=4,
            payload=diag_payload,
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(diag_frame, self.session))
        short_diag = BinaryFrame(
            msg_id=int(MessageId.RESP_DIAGNOSTICS),
            seq_num=5,
            payload=b'\x00' * 10,
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(short_diag, self.session))

        status_frame = BinaryFrame(
            msg_id=int(MessageId.RESP_STATUS),
            seq_num=6,
            payload=b'\x02',
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(status_frame, self.session))
        empty_status = BinaryFrame(
            msg_id=int(MessageId.RESP_STATUS),
            seq_num=7,
            payload=b'',
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(empty_status, self.session))

        unknown_frame = BinaryFrame(
            msg_id=999,
            seq_num=8,
            payload=b'',
            crc16=0,
        )
        self.assertFalse(self.handler.handle_frame(unknown_frame, self.session))


if __name__ == '__main__':
    main()
