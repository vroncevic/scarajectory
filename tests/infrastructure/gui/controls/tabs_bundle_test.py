# -*- coding: UTF-8 -*-

'''
Module
    tabs_bundle_test.py
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
    Unit testing for ControlsTabsBundle container.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.controls.tabs_bundle import ControlsTabsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControlsTabsBundleTestCase(TestCase):
    '''
        Unit tests for ControlsTabsBundle container.

        It defines:

            :methods:
                | test_bundle_attributes - Verifies tab instances accessibility.
                | test_bundle_immutability - Verifies frozen immutability.
    '''

    def test_bundle_attributes(self) -> None:
        '''Verifies all child tab instances are accessible via bundle properties.'''
        mock_dsl = MagicMock()
        mock_streamer = MagicMock()
        mock_val = MagicMock()
        mock_jog = MagicMock()
        mock_preview = MagicMock()

        bundle = ControlsTabsBundle(
            dsl_editor_tab=mock_dsl,
            streamer_tab=mock_streamer,
            validation_tab=mock_val,
            jog_tab=mock_jog,
            preview_tab=mock_preview,
        )
        self.assertIs(bundle.dsl_editor_tab, mock_dsl)
        self.assertIs(bundle.streamer_tab, mock_streamer)
        self.assertIs(bundle.validation_tab, mock_val)
        self.assertIs(bundle.jog_tab, mock_jog)
        self.assertIs(bundle.preview_tab, mock_preview)

    def test_bundle_immutability(self) -> None:
        '''Verifies container cannot be mutated after creation.'''
        bundle = ControlsTabsBundle(
            dsl_editor_tab=MagicMock(),
            streamer_tab=MagicMock(),
            validation_tab=MagicMock(),
            jog_tab=MagicMock(),
            preview_tab=MagicMock(),
        )
        with self.assertRaises(FrozenInstanceError):
            bundle.dsl_editor_tab = MagicMock()  # type: ignore[misc]


if __name__ == '__main__':
    main()
