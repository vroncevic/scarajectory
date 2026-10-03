# -*- coding: UTF-8 -*-

'''
Module
    binary_frame_dispatcher_test.py
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
    Unit tests for BinaryFrameDispatcher and BinaryFrameDispatcherFactory.
'''

from __future__ import annotations

from types import SimpleNamespace
from unittest import TestCase, main

from scarajectory.core.service.event.ibinary_frame_dispatcher import (
    IBinaryFrameDispatcher,
)
from scarajectory.infrastructure.event.binary_frame_dispatcher import (
    BinaryFrameDispatcher,
)
from scarajectory.infrastructure.event.binary_frame_dispatcher_factory import (
    BinaryFrameDispatcherFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubFrameHandler:
    '''
        Structural stub for binary frame handler.
    '''

    def __init__(self) -> None:
        self.handled_frames: list[object] = []

    def handle_frame(self, frame: object) -> None:
        '''Records frame for verification.'''
        self.handled_frames.append(frame)

    def get_count(self) -> int:
        '''Returns handled frames count.'''
        return len(self.handled_frames)


class BinaryFrameDispatcherTestCase(TestCase):
    '''
        Tests for BinaryFrameDispatcher routing and handler registration.

        It defines:

            :methods:
                | test_factory_and_protocol_contract - Verifies factory and protocol conformance.
                | test_register_and_dispatch_success - Verifies dispatch to registered handler.
                | test_dispatch_unregistered_message_id - Verifies dispatch returns False on unknown ID.
                | test_dispatch_invalid_payload - Verifies dispatch returns False without msg_id.
                | test_multiple_handlers_for_message - Verifies all registered handlers receive frame.
    '''

    def test_factory_and_protocol_contract(self) -> None:
        '''
            Verifies factory creation and protocol conformance.

            :exceptions: None.
        '''
        dispatcher = BinaryFrameDispatcherFactory.create()
        self.assertIsInstance(dispatcher, BinaryFrameDispatcher)
        self.assertIsInstance(dispatcher, IBinaryFrameDispatcher)
        self.assertEqual(BinaryFrameDispatcherFactory.get_version(), '1.0.4')

    def test_register_and_dispatch_success(self) -> None:
        '''
            Verifies dispatch to registered handler.

            :exceptions: None.
        '''
        dispatcher = BinaryFrameDispatcher()
        handler = StubFrameHandler()
        dispatcher.register_handler(10, handler)  # type: ignore[arg-type]

        payload = SimpleNamespace(msg_id=10, data=b'\x01\x02')
        dispatched = dispatcher.dispatch(payload)

        self.assertTrue(dispatched)
        self.assertEqual(handler.handled_frames, [payload])

    def test_dispatch_unregistered_message_id(self) -> None:
        '''
            Verifies dispatch returns False on unknown ID.

            :exceptions: None.
        '''
        dispatcher = BinaryFrameDispatcher()
        handler = StubFrameHandler()
        dispatcher.register_handler(5, handler)  # type: ignore[arg-type]

        payload = SimpleNamespace(msg_id=99, data=b'')
        dispatched = dispatcher.dispatch(payload)

        self.assertFalse(dispatched)
        self.assertEqual(handler.get_count(), 0)

    def test_dispatch_invalid_payload(self) -> None:
        '''
            Verifies dispatch returns False when payload has no msg_id attribute.

            :exceptions: None.
        '''
        dispatcher = BinaryFrameDispatcher()
        dispatched = dispatcher.dispatch('non-frame object')
        self.assertFalse(dispatched)

    def test_multiple_handlers_for_message(self) -> None:
        '''
            Verifies all registered handlers receive the dispatched frame.

            :exceptions: None.
        '''
        dispatcher = BinaryFrameDispatcher()
        handler1 = StubFrameHandler()
        handler2 = StubFrameHandler()
        dispatcher.register_handler(20, handler1)  # type: ignore[arg-type]
        dispatcher.register_handler(20, handler2)  # type: ignore[arg-type]

        payload = SimpleNamespace(msg_id=20, status='OK')
        dispatched = dispatcher.dispatch(payload)

        self.assertTrue(dispatched)
        self.assertEqual(handler1.handled_frames, [payload])
        self.assertEqual(handler2.handled_frames, [payload])


if __name__ == '__main__':
    main()
