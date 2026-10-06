# -*- coding: UTF-8 -*-

'''
Module
    iexecution_worker_test.py
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
    Unit testing for IExecutionWorker protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ExecutionWorkerStub:
    '''Structural test stub implementing IExecutionWorker.'''

    def start(self, *, session: StreamSession) -> None:
        '''Starts worker.'''

    def pause(self) -> None:
        '''Pauses worker.'''

    def resume(self) -> None:
        '''Resumes worker.'''

    def stop(self) -> None:
        '''Stops worker.'''

    def is_running(self) -> bool:
        '''Checks running status.'''
        return True


class IncompleteExecutionWorkerStub:
    '''Incomplete test stub missing is_running method.'''

    def start(self, *, session: StreamSession) -> None:
        '''Starts worker.'''


class ExecutionWorkerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IExecutionWorker.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IExecutionWorker protocol.'''
        stub = ExecutionWorkerStub()
        self.assertIsInstance(stub, IExecutionWorker)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IExecutionWorker protocol check.'''
        incomplete = IncompleteExecutionWorkerStub()
        self.assertNotIsInstance(incomplete, IExecutionWorker)


if __name__ == '__main__':
    main()
