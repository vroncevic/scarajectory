# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_frame_handler_test.py
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
    Unit tests for BinaryStreamFrameHandler and its factory.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.infrastructure.worker.binary.binary_stream_frame_handler import BinaryStreamFrameHandler
from scarajectory.infrastructure.worker.binary.binary_stream_frame_handler_factory import BinaryStreamFrameHandlerFactory
from scarajectory.infrastructure.worker.binary.ibinary_stream_frame_handler import IBinaryStreamFrameHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamFrameHandlerTestCase(TestCase):
    '''
        Tests BinaryStreamFrameHandler inbound response processing.

        It defines:

            :methods:
                | setUp - Initializes mock collaborators and handler.
                | test_ack_and_nack - Verifies ack and nack responses.
                | test_fault_event - Verifies handling of critical fault event.
                | test_factory_version - Verifies factory version string.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.

            :exceptions: None.
        '''
        self.mock_flow = MagicMock()
        self.mock_state = MagicMock()
        self.mock_dispatcher = MagicMock()
        self.frame_builder = BinaryFrameBuilderFactory.create()
        self.handler: BinaryStreamFrameHandler = (
            BinaryStreamFrameHandlerFactory.create(
                flow_pacing=self.mock_flow,
                state_controller=self.mock_state,
                observer_dispatcher=self.mock_dispatcher,
            )
        )
        self.session: StreamSession = StreamSession(
            waypoints=[],
            sent_count=1,
            done_count=0,
            failed_count=0,
            remote_queue_depth=1,
            start_time=0.0,
        )

    def test_ack_and_nack(self) -> None:
        '''Tests ACK and NACK frame handling.'''
        ack_payload = pack('<HH', 1, 0)
        ack_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_ACK),
            seq_num=1,
            payload=ack_payload,
        )
        self.assertFalse(self.handler.handle_frame(ack_frame, self.session))
        self.mock_flow.handle_binary_ack.assert_called_once_with(self.session, 0)

        nack_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_NACK),
            seq_num=2,
            payload=b'',
        )
        self.assertFalse(self.handler.handle_frame(nack_frame, self.session))
        self.assertEqual(self.session.failed_count, 1)
        self.assertEqual(self.session.remote_queue_depth, 0)

    def test_fault_event_severity_levels(self) -> None:
        '''Tests low-severity and critical-severity fault event handling.'''
        low_fault = pack('<BBI', 1, 10, 0)
        low_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_FAULT_EVENT),
            seq_num=3,
            payload=low_fault,
        )
        self.assertFalse(self.handler.handle_frame(low_frame, self.session))
        self.mock_state.set_state.assert_not_called()

        crit_fault = pack('<BBI', 2, 42, 0)
        crit_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_FAULT_EVENT),
            seq_num=4,
            payload=crit_fault,
        )
        self.assertTrue(self.handler.handle_frame(crit_frame, self.session))
        self.mock_state.set_state.assert_called_with(StreamState.STOPPED)

    def test_diagnostics_status_and_unknown(self) -> None:
        '''Tests diagnostics, status, and unhandled frames.'''
        diag_payload = b'\x00' * 52 + pack('<I', 12345)
        diag_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_DIAGNOSTICS),
            seq_num=5,
            payload=diag_payload,
        )
        self.assertFalse(self.handler.handle_frame(diag_frame, self.session))

        status_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_STATUS),
            seq_num=6,
            payload=b'\x03',
        )
        self.assertFalse(self.handler.handle_frame(status_frame, self.session))

        unknown_frame: BinaryFrame = self.frame_builder.build_frame(
            msg_id=0x99,
            seq_num=7,
            payload=b'',
        )
        self.assertFalse(self.handler.handle_frame(unknown_frame, self.session))

    def test_can_handle_and_factory(self) -> None:
        '''Tests can_handle validation, protocol adherence, and factory version.'''
        self.assertTrue(self.handler.can_handle(int(MessageId.RESP_ACK)))
        self.assertTrue(self.handler.can_handle(int(MessageId.RESP_FAULT_EVENT)))
        self.assertFalse(self.handler.can_handle(0xFF))
        self.assertIsInstance(self.handler, IBinaryStreamFrameHandler)
        self.assertEqual(BinaryStreamFrameHandlerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
