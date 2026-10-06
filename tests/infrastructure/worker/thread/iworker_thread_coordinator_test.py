# -*- coding: UTF-8 -*-

'''
Module
    iworker_thread_coordinator_test.py
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
    Unit testing for IWorkerThreadCoordinator structural protocol.
'''

from __future__ import annotations

from typing import Any, Callable
from unittest import TestCase, main

from scarajectory.infrastructure.worker.thread.iworker_thread_coordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StubWorkerThreadCoordinator:
    '''Structural stub implementing IWorkerThreadCoordinator.'''

    def start_thread(
        self,
        *,
        target: Callable[..., None],
        kwargs: dict[str, Any],
    ) -> None:
        '''Starts worker thread.'''

    def set_paused(self, *, paused: bool) -> None:
        '''Updates pause state.'''

    def stop(self) -> None:
        '''Stops worker execution.'''

    def is_running(self) -> bool:
        '''Checks active execution state.'''
        return False


class IncompleteCoordinator:
    '''Incomplete stub missing required protocol methods.'''

    def pause(self) -> None:
        '''Non-protocol pause method.'''

    def stop(self) -> None:
        '''Stops worker execution.'''


class IWorkerThreadCoordinatorTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks.'''

    def test_protocol_conformance(self) -> None:
        '''Verifies complete and incomplete coordinator protocol conformance.'''
        stub = StubWorkerThreadCoordinator()
        self.assertIsInstance(stub, IWorkerThreadCoordinator)

        incomplete = IncompleteCoordinator()
        self.assertNotIsInstance(incomplete, IWorkerThreadCoordinator)


if __name__ == '__main__':
    main()
