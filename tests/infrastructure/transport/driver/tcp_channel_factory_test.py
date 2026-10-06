# -*- coding: UTF-8 -*-

'''
Module
    tcp_channel_factory_test.py
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
    Unit testing for TcpChannelDriverFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.transport.driver.tcp_channel import TcpChannelDriver
from scarajectory.infrastructure.transport.driver.tcp_channel_factory import TcpChannelDriverFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TcpChannelDriverFactoryTestCase(TestCase):
    '''
        Unit tests for TcpChannelDriverFactory.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates TcpChannelDriver.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory instantiates a valid TcpChannelDriver object.'''
        driver = TcpChannelDriverFactory.create()
        self.assertIsInstance(driver, TcpChannelDriver)

    def test_get_version(self) -> None:
        '''Verifies factory exposes semantic version string matching package.'''
        self.assertEqual(
            TcpChannelDriverFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
