# -*- coding: UTF-8 -*-

'''
Module
    mouse_handler_bundle_test.py
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
    Unit testing for MouseHandlerBundle container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.handler.mouse_handler_bundle import (
    MouseHandlerBundle,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MouseHandlerBundleTestCase(TestCase):
    '''
        Unit tests for MouseHandlerBundle.

        It defines:

            :methods:
                | test_bundle_creation_and_attributes - Verifies bundle properties.
    '''

    def test_bundle_creation_and_attributes(self) -> None:
        '''Verifies MouseHandlerBundle stores and exposes collaborators.'''
        mock_vp = MagicMock()
        mock_state = MagicMock()
        mock_pan = MagicMock()
        mock_selection = MagicMock()
        mock_shape = MagicMock()
        mock_drag = MagicMock()

        bundle = MouseHandlerBundle(
            vp=mock_vp,
            state=mock_state,
            pan_handler=mock_pan,
            selection_handler=mock_selection,
            shape_handler=mock_shape,
            drag_handler=mock_drag,
        )

        self.assertIs(bundle.vp, mock_vp)
        self.assertIs(bundle.state, mock_state)
        self.assertIs(bundle.pan_handler, mock_pan)
        self.assertIs(bundle.selection_handler, mock_selection)
        self.assertIs(bundle.shape_handler, mock_shape)
        self.assertIs(bundle.drag_handler, mock_drag)


if __name__ == '__main__':
    main()
