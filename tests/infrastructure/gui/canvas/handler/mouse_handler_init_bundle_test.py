# -*- coding: UTF-8 -*-

'''
Module
    mouse_handler_init_bundle_test.py
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
    Unit testing for MouseHandlerInitBundle container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.mouse_handler_init_bundle import (
    MouseHandlerInitBundle,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MouseHandlerInitBundleTestCase(TestCase):
    '''
        Unit tests for MouseHandlerInitBundle.

        It defines:

            :methods:
                | test_bundle_creation_and_attributes - Verifies bundle properties.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''Verifies MouseHandlerInitBundle stores and exposes collaborators.'''
        mock_store = MagicMock()
        mock_selection = MagicMock()
        mock_mutation = MagicMock()
        mock_vp = MagicMock()
        mock_state = MagicMock()

        bundle = MouseHandlerInitBundle(
            store=mock_store,
            selection=mock_selection,
            mutation=mock_mutation,
            vp=mock_vp,
            state=mock_state,
        )

        self.assertIs(bundle.store, mock_store)
        self.assertIs(bundle.selection, mock_selection)
        self.assertIs(bundle.mutation, mock_mutation)
        self.assertIs(bundle.vp, mock_vp)
        self.assertIs(bundle.state, mock_state)


if __name__ == '__main__':
    main()
