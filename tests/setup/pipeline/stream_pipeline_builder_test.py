# -*- coding: UTF-8 -*-

'''
Module
    stream_pipeline_builder_test.py
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
    Unit tests for StreamPipelineBuilder and StreamPipelineBundle.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.connection.iconnection import IConnection
from scarajectory.infrastructure.streaming.ibinary_program_streamer import IBinaryProgramStreamer
from scarajectory.core.service.streaming.istream_dispatcher import IStreamDispatcher
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.infrastructure.connection.istream_raw_transceiver import IStreamRawTransceiver
from scarajectory.infrastructure.transport.bundle import TransportBundle
from scarajectory.infrastructure.transport.transport_factory import TransportFactory
from scarajectory.setup.pipeline.stream_pipeline_bundle import StreamPipelineBundle
from scarajectory.setup.pipeline.stream_pipeline_builder import StreamPipelineBuilder

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPipelineBuilderTestCase(TestCase):
    '''
        Tests assembling streaming pipeline components via StreamPipelineBuilder.

        It defines:

            :methods:
                | test_build_default - Verifies default bundle assembly and interfaces.
                | test_build_with_transport - Verifies bundle assembly with explicit transport.
                | test_get_version - Verifies builder version reporting.
    '''

    def test_build_default(self) -> None:
        '''
            Tests StreamPipelineBuilder.build_default assembling StreamPipelineBundle.

            :exceptions: None.
        '''
        bundle: StreamPipelineBundle = StreamPipelineBuilder.build_default()
        self.assertIsInstance(bundle, StreamPipelineBundle)
        self.assertIsInstance(bundle.connection, IConnection)
        self.assertIsInstance(bundle.raw_channel, IStreamRawTransceiver)
        self.assertIsInstance(bundle.playback_controller, IStreamPlaybackController)
        self.assertIsInstance(bundle.binary_streamer, IBinaryProgramStreamer)
        self.assertIsInstance(bundle.dispatcher, IStreamDispatcher)

    def test_build_with_transport(self) -> None:
        '''
            Tests StreamPipelineBuilder.build assembling StreamPipelineBundle with transport.

            :exceptions: None.
        '''
        transport: TransportBundle = TransportFactory.create_default_transport()
        bundle: StreamPipelineBundle = StreamPipelineBuilder.build(transport=transport)
        self.assertIsInstance(bundle, StreamPipelineBundle)
        self.assertIsInstance(bundle.connection, IConnection)
        self.assertIsInstance(bundle.raw_channel, IStreamRawTransceiver)
        self.assertIsInstance(bundle.playback_controller, IStreamPlaybackController)
        self.assertIsInstance(bundle.binary_streamer, IBinaryProgramStreamer)
        self.assertIsInstance(bundle.dispatcher, IStreamDispatcher)

    def test_get_version(self) -> None:
        '''
            Tests StreamPipelineBuilder.get_version returns expected version string.

            :exceptions: None.
        '''
        version: str = StreamPipelineBuilder.get_version()
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
