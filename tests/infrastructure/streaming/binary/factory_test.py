# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit testing for BinaryFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.streaming.binary.dependencies import BinaryDependencies
from scarajectory.infrastructure.streaming.binary.factory import BinaryFactory
from scarajectory.infrastructure.streaming.binary.istreamer import IBinaryStreamer
from scarajectory.infrastructure.streaming.binary.provides import BinaryProvides
from scarajectory.infrastructure.worker.iexecution_worker import IExecutionWorker

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryFactory(TestCase):
    '''
    Test cases verifying BinaryFactory.

    It defines:

        :methods:
            | test_create - Tests factory creates BinaryProvides with valid streamer.
            | test_get_version - Tests factory version string.
    '''

    def test_create(self) -> None:
        '''
            Tests factory creation of BinaryProvides.

            :exceptions: None.
        '''
        connection_manager = MagicMock(spec=IConnectionManager)
        state_machine = MagicMock(spec=IStreamStateMachine)
        dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        worker = MagicMock(spec=IExecutionWorker)
        session = SessionFactory.create_default()

        deps = BinaryDependencies(
            connection_manager=connection_manager,
            stream_state_machine=state_machine,
            stream_observer_dispatcher=dispatcher,
            execution_worker=worker,
            session=session,
        )

        provides: BinaryProvides = BinaryFactory.create(deps)
        self.assertIsInstance(provides, BinaryProvides)
        self.assertIsInstance(provides.binary_streamer, IBinaryStreamer)

    def test_get_version(self) -> None:
        '''
            Tests version string retrieval.

            :exceptions: None.
        '''
        self.assertEqual(BinaryFactory.get_version(), '1.0.3')
