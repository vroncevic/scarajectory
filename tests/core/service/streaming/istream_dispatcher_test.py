# -*- coding: UTF-8 -*-

'''
Module
    istream_dispatcher_test.py
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
    Unit testing for IStreamDispatcher composite protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.state.stream_state import StreamState
from scarajectory.core.service.streaming.istream_dispatcher import IStreamDispatcher
from scarajectory.core.service.streaming.observer.iobserver import IObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamDispatcherStub:
    '''Structural test stub satisfying IStreamDispatcher composite protocol.'''

    def set_observer(self, observer: IObserver) -> None:
        '''Sets observer.'''
        _ = observer

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''Dispatches log.'''
        _ = (msg, is_outgoing)

    def notify_progress(
        self,
        *,
        state: StreamState,
        session: StreamSession,
        current_line: str = '',
        error: str = '',
    ) -> None:
        '''Dispatches progress.'''
        _ = (state, session, current_line, error)


class IncompleteStreamDispatcherStub:
    '''Incomplete test stub missing progress notification method.'''

    def set_observer(self, observer: IObserver) -> None:
        '''Sets observer.'''
        _ = observer

    def notify_log(self, msg: str, is_outgoing: bool = False) -> None:
        '''Dispatches log.'''
        _ = (msg, is_outgoing)


class StreamDispatcherTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IStreamDispatcher.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies composite IStreamDispatcher protocol.'''
        stub = StreamDispatcherStub()
        self.assertIsInstance(stub, IStreamDispatcher)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails composite IStreamDispatcher protocol check.'''
        incomplete = IncompleteStreamDispatcherStub()
        self.assertNotIsInstance(incomplete, IStreamDispatcher)


if __name__ == '__main__':
    main()
