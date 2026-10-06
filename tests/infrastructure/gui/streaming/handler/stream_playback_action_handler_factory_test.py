# -*- coding: UTF-8 -*-

'''
Module
    stream_playback_action_handler_factory_test.py
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
    Unit testing for StreamPlaybackActionHandlerFactory component.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.streaming.handler.playback_handler_bundle import PlaybackHandlerBundle
from scarajectory.infrastructure.gui.streaming.handler.stream_playback_action_handler import StreamPlaybackActionHandler
from scarajectory.infrastructure.gui.streaming.handler.stream_playback_action_handler_factory import StreamPlaybackActionHandlerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPlaybackActionHandlerFactoryTestCase(TestCase):
    '''
        Unit tests for StreamPlaybackActionHandlerFactory.

        It defines:

            :methods:
                | test_create - Verifies factory instantiates StreamPlaybackActionHandler.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''Verifies factory creates StreamPlaybackActionHandler from bundle.'''
        bundle = PlaybackHandlerBundle(
            plan=MagicMock(),
            validator=MagicMock(),
            connection=MagicMock(),
            playback_controller=MagicMock(),
            progress_adapter=MagicMock(),
            port_panel=MagicMock(),
        )
        handler = StreamPlaybackActionHandlerFactory.create(bundle=bundle)
        self.assertIsInstance(handler, StreamPlaybackActionHandler)

    def test_get_version(self) -> None:
        '''Verifies factory returns version string matching module metadata.'''
        self.assertEqual(
            StreamPlaybackActionHandlerFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
