# -*- coding: UTF-8 -*-

'''
Module
    stream_raw_transceiver_factory_test.py
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
    Unit tests for StreamRawTransceiverFactory factory service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.connection.stream_raw_transceiver import (
    StreamRawTransceiver,
)
from scarajectory.infrastructure.connection.stream_raw_transceiver_factory import (
    StreamRawTransceiverFactory,
)
from scarajectory.infrastructure.transport.istream_transport_connection import (
    IStreamTransportConnection,
)
from scarajectory.infrastructure.transport.istream_transport_transceiver import (
    IStreamTransportTransceiver,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamRawTransceiverFactoryTestCase(TestCase):
    '''
        Tests StreamRawTransceiverFactory component instantiation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies instantiation of StreamRawTransceiver.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(
            StreamRawTransceiverFactory.get_version(), '1.0.4'
        )
        self.assertTrue(hasattr(StreamRawTransceiverFactory, 'create'))
        self.assertTrue(callable(StreamRawTransceiverFactory.create))

    def test_factory_create(self) -> None:
        '''Verifies create returns configured StreamRawTransceiver instance.'''
        mock_conn = MagicMock(spec=IStreamTransportConnection)
        mock_trans = MagicMock(spec=IStreamTransportTransceiver)
        transceiver = StreamRawTransceiverFactory.create(
            connection=mock_conn,
            transceiver=mock_trans,
        )
        self.assertIsInstance(transceiver, StreamRawTransceiver)


if __name__ == '__main__':
    main()
