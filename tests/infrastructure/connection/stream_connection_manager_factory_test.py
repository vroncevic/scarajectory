# -*- coding: UTF-8 -*-

'''
Module
    stream_connection_manager_factory_test.py
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
    Unit tests for StreamConnectionManagerFactory factory service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.stream_connection_manager import StreamConnectionManager
from scarajectory.infrastructure.connection.stream_connection_manager_factory import StreamConnectionManagerFactory
from scarajectory.infrastructure.transport.istream_transport_connection import IStreamTransportConnection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConnectionManagerFactoryTestCase(TestCase):
    '''
        Tests StreamConnectionManagerFactory component instantiation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies instantiation of StreamConnectionManager.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(
            StreamConnectionManagerFactory.get_version(), '1.0.3'
        )
        self.assertTrue(hasattr(StreamConnectionManagerFactory, 'create'))
        self.assertTrue(callable(StreamConnectionManagerFactory.create))

    def test_factory_create(self) -> None:
        '''Verifies create returns configured StreamConnectionManager instance.'''
        mock_conn = MagicMock(spec=IStreamTransportConnection)
        manager = StreamConnectionManagerFactory.create(
            mock_conn,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.assertIsInstance(manager, StreamConnectionManager)


if __name__ == '__main__':
    main()
