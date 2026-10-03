# -*- coding: UTF-8 -*-

'''
Module
    istream_telemetry_notifier_test.py
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
    Unit testing for IStreamTelemetryNotifier protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.infrastructure.streaming.observer.istream_telemetry_notifier import (
    IStreamTelemetryNotifier,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingNotifierStub:
    '''Conforming stub implementation satisfying IStreamTelemetryNotifier.'''

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''Dispatches log message.'''
        _ = (msg, is_outgoing)

    def notify_progress(
        self,
        *,
        state: StreamState,
        session: StreamSession,
        current_line: str = '',
        error: str = '',
    ) -> None:
        '''Dispatches stream progress.'''
        _ = (state, session, current_line, error)


class IncompleteNotifierStub:
    '''Non-conforming stub implementation missing notify_progress.'''

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''Dispatches log message.'''
        _ = (msg, is_outgoing)

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class StreamTelemetryNotifierProtocolTestCase(TestCase):
    '''
        Tests IStreamTelemetryNotifier runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamTelemetryNotifier protocol.'''
        stub = ConformingNotifierStub()
        self.assertIsInstance(stub, IStreamTelemetryNotifier)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IStreamTelemetryNotifier protocol check.'''
        stub = IncompleteNotifierStub()
        self.assertNotIsInstance(stub, IStreamTelemetryNotifier)


if __name__ == '__main__':
    main()
