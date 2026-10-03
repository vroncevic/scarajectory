# -*- coding: UTF-8 -*-

'''
Module
    istream_step_dispatcher_test.py
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
    Unit testing for IStreamStepDispatcher protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.istream_step_dispatcher import (
    IStreamStepDispatcher,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConformingStepDispatcherStub:
    '''Conforming stub implementation satisfying IStreamStepDispatcher.'''

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''Checks if step can be dispatched.'''
        _ = session
        return True

    def dispatch_step(self, session: StreamSession) -> None:
        '''Dispatches step.'''
        _ = session


class IncompleteStepDispatcherStub:
    '''Non-conforming stub implementation missing dispatch_step.'''

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''Checks if step can be dispatched.'''
        _ = session
        return False

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class StreamStepDispatcherProtocolTestCase(TestCase):
    '''
        Tests IStreamStepDispatcher runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IStreamStepDispatcher protocol.'''
        stub = ConformingStepDispatcherStub()
        self.assertIsInstance(stub, IStreamStepDispatcher)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IStreamStepDispatcher protocol check.'''
        stub = IncompleteStepDispatcherStub()
        self.assertNotIsInstance(stub, IStreamStepDispatcher)


if __name__ == '__main__':
    main()
