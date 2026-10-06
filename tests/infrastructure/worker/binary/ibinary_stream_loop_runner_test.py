# -*- coding: UTF-8 -*-

'''
Module
    ibinary_stream_loop_runner_test.py
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
    Unit testing for IBinaryStreamLoopRunner protocol specification.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main

from scaralang.core.model.dsl.binary.program import BinaryProgram
from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.binary.ibinary_stream_loop_runner import IBinaryStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStreamLoopRunnerStub:
    '''Structural test stub satisfying IBinaryStreamLoopRunner protocol.'''

    def run_waypoints_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Executes waypoints loop.'''
        _ = (session, stop_event, pause_event)

    def run_program_loop(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Executes binary program loop.'''
        _ = (session, program, stop_event, pause_event)

    def handle_incoming_bytes(
        self,
        *,
        data: bytes,
        session: StreamSession,
    ) -> bool:
        '''Processes incoming byte stream chunk.'''
        _ = (data, session)
        return False


class IncompleteBinaryStreamLoopRunnerStub:
    '''Incomplete test stub missing required run_waypoints_loop method.'''

    def run_program_loop(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Executes binary program loop.'''
        _ = (session, program, stop_event, pause_event)

    def handle_incoming_bytes(
        self,
        *,
        data: bytes,
        session: StreamSession,
    ) -> bool:
        '''Processes incoming byte stream chunk.'''
        _ = (data, session)
        return False


class BinaryStreamLoopRunnerTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IBinaryStreamLoopRunner.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IBinaryStreamLoopRunner protocol.'''
        stub = BinaryStreamLoopRunnerStub()
        self.assertIsInstance(stub, IBinaryStreamLoopRunner)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IBinaryStreamLoopRunner protocol check.'''
        incomplete = IncompleteBinaryStreamLoopRunnerStub()
        self.assertNotIsInstance(incomplete, IBinaryStreamLoopRunner)


if __name__ == '__main__':
    main()
