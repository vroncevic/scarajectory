# -*- coding: UTF-8 -*-

'''
Module
    provides_test.py
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
    Unit testing for StreamingProvides container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.streaming.binary.istreamer import IBinaryStreamer
from scarajectory.infrastructure.streaming.provides import StreamingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamingProvides(TestCase):
    '''
    Test cases verifying StreamingProvides container.

    It defines:

        :methods:
            | test_initialization - Tests attributes and immutability.
    '''

    def test_initialization(self) -> None:
        '''
            Tests initialization and immutability of StreamingProvides.

            :exceptions: None.
        '''
        connection_manager = MagicMock(spec=IConnectionManager)
        raw_channel = MagicMock(spec=IRawChannel)
        playback_controller = MagicMock(spec=IPlaybackController)
        registry = MagicMock(spec=IStreamObserverRegistry)
        dispatcher = MagicMock(spec=IStreamObserverDispatcher)
        binary_streamer = MagicMock(spec=IBinaryStreamer)

        provides = StreamingProvides(
            connection_manager=connection_manager,
            raw_channel=raw_channel,
            playback_controller=playback_controller,
            registry=registry,
            dispatcher=dispatcher,
            binary_streamer=binary_streamer,
        )

        self.assertIs(provides.connection_manager, connection_manager)
        self.assertIs(provides.raw_channel, raw_channel)
        self.assertIs(provides.playback_controller, playback_controller)
        self.assertIs(provides.registry, registry)
        self.assertIs(provides.dispatcher, dispatcher)
        self.assertIs(provides.binary_streamer, binary_streamer)


if __name__ == '__main__':
    main()
