# -*- coding: UTF-8 -*-

'''
Module
    irunner_test.py
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

from scaralang.core.model.dsl.binary.program import BinaryProgram

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.infrastructure.worker.runner.irunner import IStreamLoopRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamLoopRunnerStub:
    '''Structural test stub implementing IStreamLoopRunner.'''

    def run_waypoints_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Runs waypoints loop.'''

    def run_program_loop(
        self,
        *,
        session: StreamSession,
        program: BinaryProgram,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Runs program loop.'''

    def handle_incoming_bytes(
        self,
        *,
        data: bytes,
        session: StreamSession,
    ) -> bool:
        '''Handles incoming bytes.'''
        return len(data) > 0 and session.total_count >= 0


class IncompleteStreamLoopRunnerStub:
    '''Incomplete test stub missing handle_incoming_bytes.'''

    def run_waypoints_loop(
        self,
        *,
        session: StreamSession,
        stop_event: Event,
        pause_event: Event,
    ) -> None:
        '''Runs waypoints loop.'''

    def stop(self) -> None:
        '''Stops loop runner.'''


class StreamLoopRunnerProtocolTestCase(TestCase):
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
