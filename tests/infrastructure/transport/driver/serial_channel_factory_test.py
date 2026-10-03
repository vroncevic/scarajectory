# -*- coding: UTF-8 -*-

'''
Module
    serial_channel_factory_test.py
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
    Unit testing for SerialChannelDriverFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.transport.driver.serial_channel import (
    SerialChannelDriver,
)
from scarajectory.infrastructure.transport.driver.serial_channel_factory import (
    SerialChannelDriverFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialChannelDriverFactoryTestCase(TestCase):
    '''
        Unit tests for SerialChannelDriverFactory.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates SerialChannelDriver.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory instantiates a valid SerialChannelDriver object.'''
        driver = SerialChannelDriverFactory.create()
        self.assertIsInstance(driver, SerialChannelDriver)

    def test_get_version(self) -> None:
        '''Verifies factory exposes semantic version string matching package.'''
        self.assertEqual(
            SerialChannelDriverFactory.get_version(), '1.0.4'
        )


if __name__ == '__main__':
    main()
