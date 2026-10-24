# -*- coding: UTF-8 -*-

'''
Module
    idrainer_test.py
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
    Unit testing for IQueueDrainer protocol specification.
'''

from __future__ import annotations

from threading import Event
from unittest import TestCase, main

from scarajectory.core.model.streaming.session import StreamSession
from scarajectory.infrastructure.worker.drainer.idrainer import IQueueDrainer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueDrainerStub:
    '''Structural test stub implementing IQueueDrainer.'''

    def is_queue_empty(
        self,
        *,
        session: StreamSession,
        total_items: int,
    ) -> bool:
        '''Checks if queue empty.'''
        return session.total_count == total_items

    def drain_queue(
        self,
        *,
        session: StreamSession,
        total_items: int,
        stop_event: Event,
    ) -> None:
        '''Drains queue.'''
        if not stop_event.is_set() and session.total_count == total_items:
            return


class IncompleteQueueDrainerStub:
    '''Incomplete test stub missing drain_queue method.'''

    def is_queue_empty(
        self,
        *,
        session: StreamSession,
        total_items: int,
    ) -> bool:
        '''Checks if queue empty.'''
        return session.total_count == total_items

    def get_status(self) -> str:
        '''Gets status string.'''
        return 'incomplete'


class QueueDrainerProtocolTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IQueueDrainer.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IQueueDrainer protocol.'''
        stub = QueueDrainerStub()
        self.assertIsInstance(stub, IQueueDrainer)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IQueueDrainer protocol check.'''
        incomplete = IncompleteQueueDrainerStub()
        self.assertNotIsInstance(incomplete, IQueueDrainer)


if __name__ == '__main__':
    main()
