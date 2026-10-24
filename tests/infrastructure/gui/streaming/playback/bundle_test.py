# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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

from scarajectory.infrastructure.gui.streaming.playback.bundle import PlaybackHandlerBundle

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
        '''
            Verifies all injected collaborators are accessible via bundle properties.

            :exceptions: None.
        '''
        mock_plan = MagicMock()
        mock_validator = MagicMock()
        mock_avoidance = MagicMock()
        mock_conn = MagicMock()
        mock_playback = MagicMock()
        mock_status = MagicMock()

        bundle = PlaybackHandlerBundle(
            plan=mock_plan,
            validator=mock_validator,
            avoidance_adapter=mock_avoidance,
            connection_manager=mock_conn,
            playback_controller=mock_playback,
            status_bar=mock_status,
        )
        self.assertIs(bundle.plan, mock_plan)
        self.assertIs(bundle.validator, mock_validator)
        self.assertIs(bundle.avoidance_adapter, mock_avoidance)
        self.assertIs(bundle.connection_manager, mock_conn)
        self.assertIs(bundle.playback_controller, mock_playback)
        self.assertIs(bundle.status_bar, mock_status)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies container cannot be mutated after creation.

            :exceptions: None.
        '''
        bundle = PlaybackHandlerBundle(
            plan=MagicMock(),
            validator=MagicMock(),
            avoidance_adapter=MagicMock(),
            connection_manager=MagicMock(),
            playback_controller=MagicMock(),
            status_bar=MagicMock(),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.plan = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
