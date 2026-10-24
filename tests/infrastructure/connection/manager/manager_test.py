# -*- coding: UTF-8 -*-

'''
Module
    manager_test.py
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
    Unit testing for ConnectionManager implementation.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.connection.manager.manager import ConnectionManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionManagerTestCase(TestCase):
    '''
        Test cases for ConnectionManager component.
    '''

    def setUp(self) -> None:
        self.mock_coordinator = MagicMock()
        self.manager = ConnectionManager(
            connection_coordinator=self.mock_coordinator,
        )

    def test_protocol_compliance(self) -> None:
        '''
            Verifies ConnectionManager implements IConnectionManager.

            :exceptions: None.
        '''
        self.assertIsInstance(self.manager, IConnectionManager)

    def test_is_connected(self) -> None:
        '''
            Verifies is_connected delegates to underlying connection coordinator.

            :exceptions: None.
        '''
        self.mock_coordinator.is_connected.return_value = True
        self.assertTrue(self.manager.is_connected())
        self.mock_coordinator.is_connected.return_value = False
        self.assertFalse(self.manager.is_connected())

    def test_connect_with_config(self) -> None:
        '''
            Verifies connect_with_config calls underlying connection coordinator with config.

            :exceptions: None.
        '''
        mock_config = MagicMock()
        mock_config.port = '/dev/ttyUSB0'
        mock_config.baudrate = 115200
        self.mock_coordinator.is_connected.return_value = False
        self.mock_coordinator.connect.return_value = True
        self.assertTrue(self.manager.connect_with_config(mock_config))
        self.mock_coordinator.connect.assert_called_once_with(
            mock_config.port, mock_config.baudrate
        )

    def test_connect_with_config_when_already_connected(self) -> None:
        '''
            Verifies connect_with_config disconnects first if already connected.

            :exceptions: None.
        '''
        mock_config = MagicMock()
        mock_config.port = '/dev/ttyUSB0'
        mock_config.baudrate = 115200
        self.mock_coordinator.is_connected.return_value = True
        self.mock_coordinator.connect.return_value = True
        self.assertTrue(self.manager.connect_with_config(mock_config))
        self.mock_coordinator.disconnect.assert_called_once()
        self.mock_coordinator.connect.assert_called_once_with(
            mock_config.port, mock_config.baudrate
        )

    def test_disconnect(self) -> None:
        '''
            Verifies disconnect calls underlying disconnect.

            :exceptions: None.
        '''
        self.manager.disconnect()
        self.mock_coordinator.disconnect.assert_called_once()


if __name__ == '__main__':
    main()
