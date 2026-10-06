# -*- coding: UTF-8 -*-

'''
Module
    config_factory_test.py
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
    Unit tests for ConfigFactory creation service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.core.service.streaming.config_factory import ConfigFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestConfigFactory(TestCase):
    '''
        Test cases verifying ConfigFactory.

        It defines:

            :methods:
                | test_create_default - Verifies creating config with JSON defaults.
                | test_create_with_overrides - Verifies creating config with custom overrides.
    '''

    def test_create_default(self) -> None:
        '''
            Verifies creation with default parameters loads from JSON configuration.
        '''
        config: StreamConfig = ConfigFactory.create()
        self.assertIsInstance(config, StreamConfig)
        self.assertEqual(config.port, '/dev/ttyUSB0')
        self.assertEqual(config.baudrate, 115200)
        self.assertAlmostEqual(config.timeout, 0.1)
        self.assertEqual(config.queue_capacity, 16)

    def test_create_with_overrides(self) -> None:
        '''
            Verifies creation with custom overrides respects caller arguments.
        '''
        config: StreamConfig = ConfigFactory.create(
            port='COM3',
            baudrate=57600,
            timeout=0.5,
            queue_capacity=32,
        )
        self.assertEqual(config.port, 'COM3')
        self.assertEqual(config.baudrate, 57600)
        self.assertAlmostEqual(config.timeout, 0.5)
        self.assertEqual(config.queue_capacity, 32)


if __name__ == '__main__':
    main()
