# -*- coding: UTF-8 -*-

'''
Module
    itransport_reader_worker_test.py
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
    Unit testing for ITransportReaderWorker protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.transport.worker.itransport_reader_worker import (
    ITransportReaderWorker,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TransportReaderWorkerStub:
    '''Structural test stub satisfying ITransportReaderWorker protocol.'''

    def is_running(self) -> bool:
        '''Checks worker loop status.'''
        return True

    def run(self) -> None:
        '''Executes read loop.'''


class IncompleteTransportReaderWorkerStub:
    '''Incomplete test stub missing required run method.'''

    def is_running(self) -> bool:
        '''Checks worker loop status.'''
        return True

    def pause(self) -> None:
        '''Pauses worker.'''


class TransportReaderWorkerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for ITransportReaderWorker.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies ITransportReaderWorker protocol.'''
        stub = TransportReaderWorkerStub()
        self.assertIsInstance(stub, ITransportReaderWorker)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails ITransportReaderWorker protocol check.'''
        incomplete = IncompleteTransportReaderWorkerStub()
        self.assertNotIsInstance(incomplete, ITransportReaderWorker)


if __name__ == '__main__':
    main()
