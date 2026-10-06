# -*- coding: UTF-8 -*-

'''
Module
    playback_handler_bundle_test.py
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
    Unit testing for PlaybackHandlerBundle container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.streaming.handler.playback_handler_bundle import PlaybackHandlerBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlaybackHandlerBundleTestCase(TestCase):
    '''
        Unit tests for PlaybackHandlerBundle container.

        It defines:

            :methods:
                | test_bundle_access - Verifies container field accessibility.
                | test_bundle_immutability - Verifies frozen immutability.
    '''

    def test_bundle_access(self) -> None:
        '''Verifies all injected collaborators are accessible via bundle properties.'''
        mock_plan = MagicMock()
        mock_validator = MagicMock()
        mock_conn = MagicMock()
        mock_playback = MagicMock()
        mock_progress = MagicMock()
        mock_panel = MagicMock()

        bundle = PlaybackHandlerBundle(
            plan=mock_plan,
            validator=mock_validator,
            connection=mock_conn,
            playback_controller=mock_playback,
            progress_adapter=mock_progress,
            port_panel=mock_panel,
        )
        self.assertIs(bundle.plan, mock_plan)
        self.assertIs(bundle.validator, mock_validator)
        self.assertIs(bundle.connection, mock_conn)
        self.assertIs(bundle.playback_controller, mock_playback)
        self.assertIs(bundle.progress_adapter, mock_progress)
        self.assertIs(bundle.port_panel, mock_panel)

    def test_bundle_immutability(self) -> None:
        '''Verifies container cannot be mutated after creation.'''
        bundle = PlaybackHandlerBundle(
            plan=MagicMock(),
            validator=MagicMock(),
            connection=MagicMock(),
            playback_controller=MagicMock(),
            progress_adapter=MagicMock(),
            port_panel=MagicMock(),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.plan = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
