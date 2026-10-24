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
    Unit tests for QueueDrainerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.drainer.dependencies import QueueDrainerDependencies
from scarajectory.infrastructure.worker.drainer.drainer import QueueDrainer
from scarajectory.infrastructure.worker.drainer.factory import QueueDrainerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueDrainerFactoryTestCase(TestCase):
    '''
        Unit tests for QueueDrainerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory creates QueueDrainer instance.
                | test_version - Verifies factory get_version returns string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates QueueDrainer instance.

            :exceptions: None.
        '''
        mock_state = MagicMock(spec=IStreamStateMachine)
        mock_dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        config = StreamPacingConfig(
            poll_delay=0.001,
            send_delay=0.001,
            throttle_delay=0.001,
        )
        dependencies = QueueDrainerDependencies(
            state_controller=mock_state,
            observer_dispatcher=mock_dispatcher,
            pacing_config=config,
        )
        drainer = QueueDrainerFactory.create(dependencies)
        self.assertIsInstance(drainer, QueueDrainer)

    def test_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        self.assertEqual(QueueDrainerFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
