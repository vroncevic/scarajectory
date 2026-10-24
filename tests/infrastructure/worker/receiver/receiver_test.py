# -*- coding: UTF-8 -*-

'''
Module
    receiver_test.py
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
    Unit tests for StreamBytesReceiver implementation.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.connection.receiver.ibytes_receiver import IStreamBytesReceiver
from scarajectory.infrastructure.worker.holder import StreamSessionHolder
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker
from scarajectory.infrastructure.worker.receiver.receiver import StreamBytesReceiver
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamBytesReceiverTestCase(TestCase):
    '''
        Unit tests for StreamBytesReceiver.

        It defines:

            :methods:
                | setUp - Prepares test receiver and mock collaborators.
                | test_structural_conformance - Verifies conformance to IStreamBytesReceiver.
                | test_handle_incoming_bytes_continue - Verifies byte feeding without stop.
                | test_handle_incoming_bytes_stop - Verifies byte feeding triggers worker stop.
                | test_is_running - Verifies delegation to worker.
    '''

    def setUp(self) -> None:
        '''
            Prepares receiver and mock collaborators.

            :exceptions: None.
        '''
        self.mock_runner = MagicMock(spec=IStreamLoopRunner)
        self.mock_worker = MagicMock(spec=IExecutionWorker)
        self.session = SessionFactory.create_default()
        self.holder = StreamSessionHolder(session=self.session)
        self.receiver = StreamBytesReceiver(
            loop_runner=self.mock_runner,
            worker=self.mock_worker,
            session_holder=self.holder,
        )

    def test_structural_conformance(self) -> None:
        '''
            Verifies receiver satisfies IStreamBytesReceiver structurally.

            :exceptions: None.
        '''
        self.assertIsInstance(self.receiver, IStreamBytesReceiver)

    def test_handle_incoming_bytes_continue(self) -> None:
        '''
            Verifies normal byte handling doesn't stop worker.

            :exceptions: None.
        '''
        self.mock_runner.handle_incoming_bytes.return_value = False
        self.receiver.handle_incoming_bytes(b'\x01\x02')
        self.mock_runner.handle_incoming_bytes.assert_called_once_with(
            data=b'\x01\x02', session=self.session
        )
        self.mock_worker.stop.assert_not_called()

    def test_handle_incoming_bytes_stop(self) -> None:
        '''
            Verifies critical byte handling stops worker.

            :exceptions: None.
        '''
        self.mock_runner.handle_incoming_bytes.return_value = True
        self.receiver.handle_incoming_bytes(b'\xFF')
        self.mock_runner.handle_incoming_bytes.assert_called_once_with(
            data=b'\xFF', session=self.session
        )
        self.mock_worker.stop.assert_called_once()

    def test_is_running(self) -> None:
        '''
            Verifies is_running delegates to worker.

            :exceptions: None.
        '''
        self.mock_worker.is_running.return_value = True
        self.assertTrue(self.receiver.is_running())
        self.mock_worker.is_running.assert_called_once()


if __name__ == '__main__':
    main()
