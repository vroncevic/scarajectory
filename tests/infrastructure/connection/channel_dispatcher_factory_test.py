# -*- coding: UTF-8 -*-

'''
Module
    channel_dispatcher_factory_test.py
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
    Unit tests for ChannelDispatcherFactory factory service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.iraw_channel import IRawChannel
from scarajectory.infrastructure.connection.channel_dispatcher import ChannelDispatcher
from scarajectory.infrastructure.connection.channel_dispatcher_factory import ChannelDispatcherFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ChannelDispatcherFactoryTestCase(TestCase):
    '''
        Tests ChannelDispatcherFactory component instantiation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies instantiation of ChannelDispatcher.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(ChannelDispatcherFactory.get_version(), '1.0.3')
        self.assertTrue(hasattr(ChannelDispatcherFactory, 'create'))
        self.assertTrue(callable(ChannelDispatcherFactory.create))

    def test_factory_create(self) -> None:
        '''Verifies create returns configured ChannelDispatcher instance.'''
        mock_channel = MagicMock(spec=IRawChannel)
        mock_builder = MagicMock(spec=IBinaryFrameBuilder)
        dispatcher = ChannelDispatcherFactory.create(
            raw_channel=mock_channel,
            frame_builder=mock_builder,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.assertIsInstance(dispatcher, ChannelDispatcher)


if __name__ == '__main__':
    main()
