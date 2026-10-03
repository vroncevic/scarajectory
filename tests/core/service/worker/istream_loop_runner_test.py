# -*- coding: UTF-8 -*-

'''
Module
    istream_loop_runner_test.py
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
    Unit testing for IStreamLoopRunner protocol specification.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.service.worker.istream_loop_runner import IStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLoopRunnerStub:
    '''Structural test stub satisfying IStreamLoopRunner protocol.'''

    def run_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Executes streaming loop.'''
        _ = (session, stop_event, pause_event)

    def handle_incoming_line(
        self,
        line: str,
        *,
        session: StreamSession,
    ) -> bool:
        '''Processes incoming line.'''
        _ = (line, session)
        return False


class IncompleteStreamLoopRunnerStub:
    '''Incomplete test stub missing required run_loop method.'''

    def process_data(self, data: str) -> bool:
        '''Alternative process handler.'''
        return len(data) > 0

    def handle_incoming_line(
        self,
        line: str,
        *,
        session: StreamSession,
    ) -> bool:
        '''Processes incoming line.'''
        _ = (line, session)
        return False


class StreamLoopRunnerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamLoopRunner.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamLoopRunner protocol.'''
        stub = StreamLoopRunnerStub()
        self.assertIsInstance(stub, IStreamLoopRunner)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IStreamLoopRunner protocol check.'''
        incomplete = IncompleteStreamLoopRunnerStub()
        self.assertNotIsInstance(incomplete, IStreamLoopRunner)


if __name__ == '__main__':
    main()
