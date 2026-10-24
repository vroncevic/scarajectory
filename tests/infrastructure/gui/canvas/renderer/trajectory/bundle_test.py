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
    Unit tests for TrajectoryRenderBundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.renderer.trajectory.bundle import TrajectoryRenderBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectoryRenderBundleTestCase(TestCase):
    '''
        Test cases for TrajectoryRenderBundle immutability and attributes.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle and accessing properties.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Tests creating bundle and accessing properties.

            :exceptions: None.
        '''
        mock_store = MagicMock()
        mock_selection = MagicMock()
        mock_validator = MagicMock()

        bundle = TrajectoryRenderBundle(
            store=mock_store,
            selection=mock_selection,
            validator=mock_validator,
        )

        self.assertIs(bundle.store, mock_store)
        self.assertIs(bundle.selection, mock_selection)
        self.assertIs(bundle.validator, mock_validator)


if __name__ == '__main__':
    main()
