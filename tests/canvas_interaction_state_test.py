# -*- coding: UTF-8 -*-

'''
Module
    canvas_interaction_state_test.py
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
    Unit tests for CanvasInteractionState.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.canvas_interaction_state import CanvasInteractionState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCanvasInteractionState(unittest.TestCase):
    '''
        Test cases for CanvasInteractionState.

        It defines:

            :methods:
                | test_initial_state - Tests default values of interaction state.
                | test_reset_drag - Tests resetting drag attributes.
                | test_reset_pan - Tests resetting pan attributes.
    '''

    def test_initial_state(self) -> None:
        '''
            Tests default state variables.

            :exceptions: None.
        '''
        state = CanvasInteractionState()
        self.assertEqual(state.pan_x, 0)
        self.assertEqual(state.pan_y, 0)
        self.assertFalse(state.is_panning)
        self.assertIsNone(state.drag_start_world)
        self.assertIsNone(state.drag_current_world)
        self.assertEqual(state.dragged_node_idx, -1)

    def test_reset_drag(self) -> None:
        '''
            Tests reset_drag clearing operations.

            :exceptions: None.
        '''
        state = CanvasInteractionState(
            drag_start_world=(10.0, 20.0),
            drag_current_world=(15.0, 25.0),
            dragged_node_idx=3
        )
        state.reset_drag()
        self.assertIsNone(state.drag_start_world)
        self.assertIsNone(state.drag_current_world)
        self.assertEqual(state.dragged_node_idx, -1)

    def test_reset_pan(self) -> None:
        '''
            Tests reset_pan clearing operations.

            :exceptions: None.
        '''
        state = CanvasInteractionState(pan_x=100, pan_y=200, is_panning=True)
        state.reset_pan()
        self.assertEqual(state.pan_x, 0)
        self.assertEqual(state.pan_y, 0)
        self.assertFalse(state.is_panning)


if __name__ == '__main__':
    unittest.main()
