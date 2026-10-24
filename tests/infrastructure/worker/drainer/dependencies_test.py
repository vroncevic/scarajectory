# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for QueueDrainerDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.drainer.dependencies import QueueDrainerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class QueueDrainerDependenciesTestCase(TestCase):
    '''
        Unit tests for QueueDrainerDependencies.

        It defines:

            :methods:
                | test_initialization - Verifies attributes storage in parameter bundle.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies attributes storage in parameter bundle.

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
        self.assertIs(dependencies.state_controller, mock_state)
        self.assertIs(dependencies.observer_dispatcher, mock_dispatcher)
        self.assertIs(dependencies.pacing_config, config)


if __name__ == '__main__':
    main()
