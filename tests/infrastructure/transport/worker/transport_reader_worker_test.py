# -*- coding: UTF-8 -*-

'''
Module
    transport_reader_worker_test.py
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
    Unit tests for TransportReaderWorker component.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main

from scarajectory.infrastructure.transport.worker.transport_reader_worker import (
    TransportReaderWorker,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubChannelDriver:
    '''
        Structural stub for channel driver.
    '''

    def __init__(
        self, data_chunks: list[bytes], raise_on_read: bool = False
    ) -> None:
        self.data_chunks: list[bytes] = data_chunks
        self.raise_on_read: bool = raise_on_read
        self.closed: bool = False
        self.open_state: bool = True

    def is_open(self) -> bool:
        '''Checks channel state.'''
        return self.open_state

    def read_bytes(self, size: int) -> bytes:
        '''Reads simulated bytes.'''
        del size
        if self.raise_on_read:
            raise OSError('Driver read failure')
        if self.data_chunks:
            return self.data_chunks.pop(0)
        return b''

    def write_bytes(self, data: bytes) -> int:
        '''Writes bytes.'''
        return len(data)

    def open_channel(self) -> bool:
        '''Opens channel.'''
        self.open_state = True
        return True

    def close_channel(self) -> None:
        '''Closes channel.'''
        self.open_state = False
        self.closed = True


class StubTransportListener:
    '''
        Structural stub for transport event listener.
    '''

    def __init__(self, raise_in_callbacks: bool = False) -> None:
        self.raise_in_callbacks: bool = raise_in_callbacks
        self.bytes_received: list[bytes] = []
        self.lines_received: list[str] = []
        self.logs: list[tuple[str, bool]] = []

    def on_bytes_received(self, data: bytes) -> None:
        '''Receives raw bytes.'''
        if self.raise_in_callbacks:
            raise RuntimeError('Byte callback fault')
        self.bytes_received.append(data)

    def on_line_received(self, line: str) -> None:
        '''Receives parsed line.'''
        if self.raise_in_callbacks:
            raise RuntimeError('Packet callback fault')
        self.lines_received.append(line)

    def on_log_emitted(self, message: str, is_error: bool) -> None:
        '''Receives log messages.'''
        self.logs.append((message, is_error))


class TransportReaderWorkerTestCase(TestCase):
    '''
        Test cases verifying TransportReaderWorker behavior.

        It defines:

            :methods:
                | test_is_running_and_closed_driver - Tests running state and closed driver exit.
                | test_run_processes_incoming_stream - Tests byte and line dispatching and empty read.
                | test_run_handles_abnormal_disconnect - Tests disconnect and clean shutdown paths.
                | test_run_catches_listener_exceptions - Tests error recovery when listener raises.
    '''

    def test_is_running_and_closed_driver(self) -> None:
        '''Verifies is_running reflects stop event and run exits on closed driver.'''
        stop_event: Event = Event()
        driver = StubChannelDriver([])
        listener = StubTransportListener()
        worker = TransportReaderWorker(
            stop_event=stop_event,
            driver=driver,
            listener=listener,
        )
        self.assertTrue(worker.is_running())
        stop_event.set()
        self.assertFalse(worker.is_running())

        stop_event.clear()
        driver.open_state = False
        worker.run()
        self.assertFalse(driver.closed)

    def test_run_processes_incoming_stream(self) -> None:
        '''Verifies read loop forwards raw bytes and splits newline lines with empty pause.'''
        stop_event: Event = Event()
        driver = StubChannelDriver([b'', b'HELLO\nWORLD\n'])
        listener = StubTransportListener()
        worker = TransportReaderWorker(
            stop_event=stop_event,
            driver=driver,
            listener=listener,
        )

        def stop_after_chunks(line: str) -> None:
            if line == 'WORLD':
                stop_event.set()

        listener.on_line_received = stop_after_chunks
        worker.run()
        self.assertFalse(worker.is_running())

    def test_run_handles_abnormal_disconnect(self) -> None:
        '''Verifies driver close and notification on abnormal vs normal I/O error.'''
        stop_event: Event = Event()
        driver = StubChannelDriver([], raise_on_read=True)
        listener = StubTransportListener()
        worker = TransportReaderWorker(
            stop_event=stop_event,
            driver=driver,
            listener=listener,
        )
        worker.run()
        self.assertTrue(driver.closed)
        self.assertTrue(
            any('Connection lost' in msg for msg, _ in listener.logs)
        )

        stop_event_normal: Event = Event()
        stop_event_normal.set()
        driver_normal = StubChannelDriver([], raise_on_read=True)
        listener_normal = StubTransportListener()
        worker_normal = TransportReaderWorker(
            stop_event=stop_event_normal,
            driver=driver_normal,
            listener=listener_normal,
        )
        worker_normal.run()
        self.assertFalse(driver_normal.closed)

    def test_run_catches_listener_exceptions(self) -> None:
        '''Verifies listener callback errors are safely logged without crashing.'''
        stop_event: Event = Event()
        driver = StubChannelDriver([b'TEST\n'])
        listener = StubTransportListener(raise_in_callbacks=True)
        worker = TransportReaderWorker(
            stop_event=stop_event,
            driver=driver,
            listener=listener,
        )

        def on_log_emitted_handler(msg: str, is_err: bool) -> None:
            listener.logs.append((msg, is_err))
            if 'Packet callback error' in msg:
                stop_event.set()

        listener.on_log_emitted = on_log_emitted_handler
        worker.run()
        self.assertTrue(
            any('Byte callback error' in msg for msg, _ in listener.logs)
        )
        self.assertTrue(
            any('Packet callback error' in msg for msg, _ in listener.logs)
        )


if __name__ == '__main__':
    main()
