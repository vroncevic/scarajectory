# -*- coding: UTF-8 -*-

'''
Module
    stream_pipeline_assembler_test.py
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
    Unit tests for StreamPipelineAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.transport.itransport import ITransport

from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.provides import StreamingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamPipelineAssembler(TestCase):
    '''
        Test cases verifying StreamPipelineAssembler behavior.

        It defines:

            :methods:
                | test_assemble_pipeline - Tests assembling pipeline with explicit transport.
                | test_assemble_default - Tests assemble_default helper.
                | test_get_version - Tests get_version return value.
    '''

    def test_assemble_pipeline(self) -> None:
        '''
            Tests assembling pipeline with mock transport.

            :exceptions: None.
        '''
        mock_transport = MagicMock(spec=ITransport)
        mock_transport.is_connected.return_value = False
        bundle = StreamPipelineAssembler.assemble(
            transport=mock_transport,
            queue_capacity=10,
        )
        self.assertIsInstance(bundle, StreamingProvides)

    def test_assemble_default(self) -> None:
        '''
            Tests assemble_default factory method.

            :exceptions: None.
        '''
        mock_transport = MagicMock(spec=ITransport)
        mock_transport.is_connected.return_value = False

        with patch(
            'scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler.TransportFactory.create',
            return_value=mock_transport,
        ):
            bundle = StreamPipelineAssembler.assemble_default(
                queue_capacity=5,
            )
            self.assertIsInstance(bundle, StreamingProvides)

    def test_get_version(self) -> None:
        '''
            Tests get_version returns semantic version string.

            :exceptions: None.
        '''
        ver = StreamPipelineAssembler.get_version()
        self.assertIsInstance(ver, str)
        self.assertTrue(len(ver) > 0)


if __name__ == '__main__':
    main()
