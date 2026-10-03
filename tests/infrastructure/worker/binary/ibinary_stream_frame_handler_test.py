# -*- coding: UTF-8 -*-

'''
Module
    ibinary_stream_frame_handler_test.py
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
    Unit testing for IBinaryStreamFrameHandler protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.binary.ibinary_stream_frame_handler import (
    IBinaryStreamFrameHandler,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamFrameHandlerStub:
    '''Structural test stub satisfying IBinaryStreamFrameHandler protocol.'''

    def can_handle(self, msg_id: int) -> bool:
        '''Checks message ID support.'''
        return msg_id > 0

    def handle_frame(self, frame: BinaryFrame, session: StreamSession) -> bool:
        '''Handles incoming binary frame.'''
        _ = (frame, session)
        return False


class IncompleteBinaryStreamFrameHandlerStub:
    '''Incomplete test stub missing required handle_frame method.'''

    def can_handle(self, msg_id: int) -> bool:
        '''Checks message ID support.'''
        return msg_id > 0

    def get_supported_ids(self) -> list[int]:
        '''Returns supported ids.'''
        return [1, 2]


class BinaryStreamFrameHandlerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IBinaryStreamFrameHandler.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IBinaryStreamFrameHandler protocol.'''
        stub = BinaryStreamFrameHandlerStub()
        self.assertIsInstance(stub, IBinaryStreamFrameHandler)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IBinaryStreamFrameHandler protocol check.'''
        incomplete = IncompleteBinaryStreamFrameHandlerStub()
        self.assertNotIsInstance(incomplete, IBinaryStreamFrameHandler)


if __name__ == '__main__':
    main()
