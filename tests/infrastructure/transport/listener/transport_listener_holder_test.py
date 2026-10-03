# -*- coding: UTF-8 -*-

'''
Module
    transport_listener_holder_test.py
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
    Unit tests for TransportListenerHolder dynamic transport event wrapper.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.transport.listener.itransport_listener_holder import (
    ITransportListenerHolder,
)
from scarajectory.infrastructure.transport.listener.transport_listener_holder import (
    TransportListenerHolder,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubListener:
    '''
        Structural stub for transport listener.
    '''

    def __init__(self) -> None:
        self.lines: list[str] = []
        self.bytes_data: list[bytes] = []
        self.logs: list[tuple[str, bool]] = []

    def on_line_received(self, line: str) -> None:
        '''Records line event.'''
        self.lines.append(line)

    def on_bytes_received(self, data: bytes) -> None:
        '''Records bytes event.'''
        self.bytes_data.append(data)

    def on_log_emitted(self, message: str, is_sent: bool) -> None:
        '''Records log event.'''
        self.logs.append((message, is_sent))


class TransportListenerHolderTestCase(TestCase):
    '''
        Tests for TransportListenerHolder delegation and dynamic replacement.

        It defines:

            :methods:
                | test_protocol_conformance - Verifies structural protocol matching.
                | test_delegation_to_listener - Verifies event routing to active listener.
                | test_dynamic_listener_switch - Verifies updating listener target via set_listener.
    '''

    def test_protocol_conformance(self) -> None:
        '''
            Verifies structural protocol matching.

            :exceptions: None.
        '''
        listener = StubListener()
        holder = TransportListenerHolder(listener)  # type: ignore[arg-type]
        self.assertIsInstance(holder, ITransportListenerHolder)

    def test_delegation_to_listener(self) -> None:
        '''
            Verifies event routing to active listener.

            :exceptions: None.
        '''
        listener = StubListener()
        holder = TransportListenerHolder(listener)  # type: ignore[arg-type]

        holder.on_line_received('G0 X0 Y0')
        holder.on_bytes_received(b'\xAA\xBB')
        holder.on_log_emitted('Sent command', True)

        self.assertEqual(listener.lines, ['G0 X0 Y0'])
        self.assertEqual(listener.bytes_data, [b'\xAA\xBB'])
        self.assertEqual(listener.logs, [('Sent command', True)])

    def test_dynamic_listener_switch(self) -> None:
        '''
            Verifies updating listener target via set_listener.

            :exceptions: None.
        '''
        listener_a = StubListener()
        listener_b = StubListener()
        holder = TransportListenerHolder(listener_a)  # type: ignore[arg-type]

        holder.on_line_received('Message A')
        self.assertEqual(listener_a.lines, ['Message A'])
        self.assertEqual(listener_b.lines, [])

        holder.set_listener(listener_b)  # type: ignore[arg-type]
        holder.on_line_received('Message B')
        self.assertEqual(listener_a.lines, ['Message A'])
        self.assertEqual(listener_b.lines, ['Message B'])


if __name__ == '__main__':
    main()
