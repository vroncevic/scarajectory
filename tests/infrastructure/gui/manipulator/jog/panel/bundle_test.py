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
    Unit tests for JogPanelBundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.jog.panel.bundle import JogPanelBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogPanelBundle(TestCase):
    '''
        Test cases verifying JogPanelBundle instantiation and property access.
    '''

    def test_bundle_properties(self) -> None:
        '''
            Tests bundle attributes assignment.

            :exceptions: None.
        '''
        mock_power = MagicMock()
        mock_grid = MagicMock()
        mock_tool = MagicMock()
        mock_raw = MagicMock()

        bundle = JogPanelBundle(
            power_panel=mock_power,
            axis_grid_panel=mock_grid,
            tool_panel=mock_tool,
            raw_panel=mock_raw,
        )

        self.assertIs(bundle.power_panel, mock_power)
        self.assertIs(bundle.axis_grid_panel, mock_grid)
        self.assertIs(bundle.tool_panel, mock_tool)
        self.assertIs(bundle.raw_panel, mock_raw)


if __name__ == '__main__':
    main()
