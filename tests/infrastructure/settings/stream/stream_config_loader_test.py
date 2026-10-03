# -*- coding: UTF-8 -*-

'''
Module
    stream_config_loader_test.py
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
    Unit tests for StreamConfigLoader and StreamConfigLoaderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.core.service.settings.istream_config_loader import IStreamConfigLoader
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory
from scarajectory.infrastructure.settings.stream.stream_config_loader import StreamConfigLoader
from scarajectory.infrastructure.settings.stream.stream_config_loader_factory import StreamConfigLoaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamConfigLoader(TestCase):
    '''
        Unit test cases verifying StreamConfigLoader and factory.

        It defines:

            :methods:
                | setUp - Initializes loader fixture.
                | test_factory_interface - Verifies factory returns IStreamConfigLoader protocol.
                | test_factory_create_with_reader - Verifies factory creation with explicit reader.
                | test_factory_version - Verifies factory version string.
                | test_load_stream_config - Verifies stream config creation from JSON configuration.
                | test_load_stream_config_with_options - Verifies override options in stream config.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing StreamConfigLoader via factory.
        '''
        self.loader: IStreamConfigLoader = StreamConfigLoaderFactory.create()

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs an instance satisfying IStreamConfigLoader.
        '''
        self.assertIsInstance(self.loader, IStreamConfigLoader)

    def test_factory_create_with_reader(self) -> None:
        '''
            Verifies factory constructs instance with explicit reader.
        '''
        loader: StreamConfigLoader = (
            StreamConfigLoaderFactory.create_with_reader(
                reader=SettingsReaderFactory.create()
            )
        )
        self.assertIsInstance(loader, IStreamConfigLoader)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(StreamConfigLoaderFactory.get_version(), str)

    def test_load_stream_config(self) -> None:
        '''
            Verifies load_stream_config returns pure StreamConfig from JSON SSoT.
        '''
        config: StreamConfig = self.loader.load_stream_config(port='/dev/ttyUSB0')
        self.assertIsInstance(config, StreamConfig)
        self.assertEqual(config.port, '/dev/ttyUSB0')
        self.assertEqual(config.baudrate, 115200)
        self.assertAlmostEqual(config.timeout, 0.1)

    def test_load_stream_config_with_options(self) -> None:
        '''
            Verifies options override values from JSON in stream config model.
        '''
        config: StreamConfig = self.loader.load_stream_config_with_options(
            port='COM5',
            options={'baudrate': 9600.0, 'timeout': 1.5}
        )
        self.assertEqual(config.port, 'COM5')
        self.assertEqual(config.baudrate, 9600)
        self.assertAlmostEqual(config.timeout, 1.5)


if __name__ == '__main__':
    main()
