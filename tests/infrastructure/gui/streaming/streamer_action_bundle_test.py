# -*- coding: UTF-8 -*-

'''
Module
    streamer_action_bundle_test.py
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
    Unit testing for StreamerActionBundle container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.streaming.streamer_action_bundle import (
    StreamerActionBundle,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamerActionBundleTestCase(TestCase):
    '''
        Unit tests for StreamerActionBundle container.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies bundle properties accessibility.
                | test_bundle_immutability - Verifies frozen immutability.
    '''

    def test_bundle_attributes(self) -> None:
        '''Verifies all action handlers are accessible via bundle properties.'''
        mock_playback = MagicMock()
        mock_tool = MagicMock()

        bundle = StreamerActionBundle(
            playback_handler=mock_playback,
            tool_handler=mock_tool,
        )
        self.assertIs(bundle.playback_handler, mock_playback)
        self.assertIs(bundle.tool_handler, mock_tool)

    def test_bundle_immutability(self) -> None:
        '''Verifies container cannot be mutated after creation.'''
        bundle = StreamerActionBundle(
            playback_handler=MagicMock(),
            tool_handler=MagicMock(),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.playback_handler = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
