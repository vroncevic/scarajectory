# -*- coding: UTF-8 -*-

'''
Module
    icoordinator_test.py
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
    Unit testing for IWorkerThreadCoordinator protocol specification.
'''

from __future__ import annotations

from collections.abc import Callable, Mapping
from unittest import TestCase, main

from scarajectory.infrastructure.worker.thread.icoordinator import IWorkerThreadCoordinator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WorkerThreadCoordinatorStub:
    '''Structural test stub implementing IWorkerThreadCoordinator.'''

    def start_thread(
        self,
        *,
        target: Callable[..., None],
        kwargs: Mapping[str, object],
    ) -> None:
        '''Starts thread.'''

    def set_paused(self, *, paused: bool) -> None:
        '''Sets paused state.'''

    def stop(self) -> None:
        '''Stops thread.'''

    def is_running(self) -> bool:
        '''Checks running state.'''
        return True


class IncompleteWorkerThreadCoordinatorStub:
    '''Incomplete test stub missing is_running method.'''

    def start_thread(
        self,
        *,
        target: Callable[..., None],
        kwargs: Mapping[str, object],
    ) -> None:
        '''Starts thread.'''

    def stop(self) -> None:
        '''Stops thread.'''


class WorkerThreadCoordinatorProtocolTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IWorkerThreadCoordinator.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IWorkerThreadCoordinator protocol.'''
        stub = WorkerThreadCoordinatorStub()
        self.assertIsInstance(stub, IWorkerThreadCoordinator)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IWorkerThreadCoordinator protocol check.'''
        incomplete = IncompleteWorkerThreadCoordinatorStub()
        self.assertNotIsInstance(incomplete, IWorkerThreadCoordinator)


if __name__ == '__main__':
    main()
