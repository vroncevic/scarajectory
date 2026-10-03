# -*- coding: UTF-8 -*-

'''
Module
    stream_pacing_config_test.py
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
    Unit tests for StreamPacingConfig loop timing and delay data model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.streaming.stream_pacing_config import (
    StreamPacingConfig,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPacingConfigTestCase(TestCase):
    '''
        Tests for StreamPacingConfig immutable delay parameters container.

        It defines:

            :methods:
                | test_config_creation - Verifies attribute assignment upon creation.
                | test_config_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across identical instances.
    '''

    def test_config_creation(self) -> None:
        '''
            Verifies attribute assignment upon creation.

            :exceptions: None.
        '''
        config = StreamPacingConfig(
            send_delay=0.005,
            throttle_delay=0.02,
            poll_delay=0.01,
        )
        self.assertEqual(config.send_delay, 0.005)
        self.assertEqual(config.throttle_delay, 0.02)
        self.assertEqual(config.poll_delay, 0.01)

    def test_config_immutability(self) -> None:
        '''
            Verifies frozen instance constraints.

            :exceptions: None.
        '''
        config = StreamPacingConfig(
            send_delay=0.01,
            throttle_delay=0.05,
            poll_delay=0.02,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(config, 'send_delay', 0.1)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical instances.

            :exceptions: None.
        '''
        c1 = StreamPacingConfig(
            send_delay=0.001,
            throttle_delay=0.01,
            poll_delay=0.005,
        )
        c2 = StreamPacingConfig(
            send_delay=0.001,
            throttle_delay=0.01,
            poll_delay=0.005,
        )
        self.assertEqual(c1, c2)


if __name__ == '__main__':
    main()
