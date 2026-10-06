# -*- coding: UTF-8 -*-

'''
Module
    stream_queue_drainer_factory_test.py
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
    Unit tests for StreamQueueDrainerFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.worker.ascii.stream_queue_drainer import StreamQueueDrainer
from scarajectory.infrastructure.worker.ascii.stream_queue_drainer_factory import StreamQueueDrainerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamQueueDrainerFactory(TestCase):
    '''
        Test cases verifying StreamQueueDrainerFactory behavior.

        It defines:

            :methods:
                | test_create - Tests create factory method.
                | test_get_version - Tests get_version return value.
    '''

    def test_create(self) -> None:
        '''
            Tests create factory method.

            :exceptions: None.
        '''
        pacing_config = StreamPacingConfigFactory.create_ascii()
        drainer = StreamQueueDrainerFactory.create(
            state_controller=MagicMock(),
            observer_dispatcher=MagicMock(),
            pacing_config=pacing_config,
        )
        self.assertIsInstance(drainer, StreamQueueDrainer)

    def test_get_version(self) -> None:
        '''
            Tests get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = StreamQueueDrainerFactory.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
