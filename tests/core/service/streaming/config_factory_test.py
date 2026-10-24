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
    Unit testing for ConfigFactory streaming configuration factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.core.service.streaming.config_factory import ConfigFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigFactoryTestCase(TestCase):
    '''Unit tests for ConfigFactory creation and version verification.'''

    def test_create_default(self) -> None:
        '''
            Verifies ConfigFactory creates StreamConfig with defaults.

            :exceptions: None.
        '''
        cfg: StreamConfig = ConfigFactory.create_default()
        self.assertEqual(cfg.port, ConfigFactory.DEFAULT_PORT)
        self.assertEqual(cfg.baudrate, ConfigFactory.DEFAULT_BAUDRATE)
        self.assertEqual(cfg.timeout, ConfigFactory.DEFAULT_TIMEOUT)
        self.assertEqual(cfg.queue_capacity, ConfigFactory.DEFAULT_QUEUE_CAPACITY)

    def test_create_explicit(self) -> None:
        '''
            Verifies ConfigFactory creates StreamConfig with explicit parameters.

            :exceptions: None.
        '''
        cfg: StreamConfig = ConfigFactory.create(
            port='192.168.1.50:8888',
            baudrate=230400,
        )
        self.assertEqual(cfg.port, '192.168.1.50:8888')
        self.assertEqual(cfg.baudrate, 230400)
        self.assertEqual(cfg.timeout, ConfigFactory.DEFAULT_TIMEOUT)
        self.assertEqual(cfg.queue_capacity, ConfigFactory.DEFAULT_QUEUE_CAPACITY)

    def test_get_version(self) -> None:
        '''
            Verifies ConfigFactory returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(ConfigFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
