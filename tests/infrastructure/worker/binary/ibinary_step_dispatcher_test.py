# -*- coding: UTF-8 -*-

'''
Module
    ibinary_step_dispatcher_test.py
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
    Unit testing for IBinaryStepDispatcher protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.dsl.binary.step import Step

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.infrastructure.worker.binary.ibinary_step_dispatcher import IBinaryStepDispatcher

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class BinaryStepDispatcherStub:
    '''Structural test stub satisfying IBinaryStepDispatcher protocol.'''

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''Checks if step can be dispatched.'''
        _ = session
        return True

    def dispatch_waypoint(self, session: StreamSession) -> None:
        '''Dispatches waypoint.'''
        _ = session

    def dispatch_binary_step(
        self,
        *,
        session: StreamSession,
        step: Step,
    ) -> None:
        '''Dispatches binary step.'''
        _ = (session, step)


class IncompleteBinaryStepDispatcherStub:
    '''Incomplete test stub missing dispatch_waypoint method.'''

    def can_dispatch_step(self, session: StreamSession) -> bool:
        '''Checks if step can be dispatched.'''
        _ = session
        return True

    def dispatch_binary_step(
        self,
        *,
        session: StreamSession,
        step: Step,
    ) -> None:
        '''Dispatches binary step.'''
        _ = (session, step)


class BinaryStepDispatcherProtocolTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IBinaryStepDispatcher.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IBinaryStepDispatcher protocol.'''
        stub = BinaryStepDispatcherStub()
        self.assertIsInstance(stub, IBinaryStepDispatcher)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IBinaryStepDispatcher protocol check.'''
        incomplete = IncompleteBinaryStepDispatcherStub()
        self.assertNotIsInstance(incomplete, IBinaryStepDispatcher)


if __name__ == '__main__':
    main()
