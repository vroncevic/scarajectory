# -*- coding: UTF-8 -*-

'''
Module
    jog_axis_grid_panel_test.py
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
    Unit tests for JogAxisGridPanel and JogAxisGridPanelFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.model.jog.jog_axis import JogAxis
from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel import JogAxisGridPanel
from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel_factory import JogAxisGridPanelFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogAxisGridPanel(TestCase):
    '''
        Test cases verifying JogAxisGridPanel step selection and directional jog steps.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def setUp(self) -> None:
        self.mock_jog = MagicMock()
        self.mock_query = MagicMock()
        self.panel: JogAxisGridPanel = JogAxisGridPanelFactory.create(
            self.root,
            jog_controller=self.mock_jog,
            query_controller=self.mock_query,
        )

    def tearDown(self) -> None:
        self.panel.destroy()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(JogAxisGridPanelFactory.get_version(), '1.0.4')

    def test_step_size_accessors(self) -> None:
        '''
            Tests get_step_size and set_step_size methods.
        '''
        self.assertEqual(self.panel.get_step_size(), 10.0)
        self.panel.set_step_size(25.0)
        self.assertEqual(self.panel.get_step_size(), 25.0)

    def test_jog_step_positive(self) -> None:
        '''
            Tests jog step along X axis with default positive sign.
        '''
        self.panel.jog_step(JogAxis.X, 1.0)
        self.mock_jog.jog.assert_called_once_with('X', 10.0)
        self.mock_query.query_status.assert_called_once()

    def test_jog_step_negative(self) -> None:
        '''
            Tests jog step along Y axis with negative sign and updated step size.
        '''
        self.panel.set_step_size(5.0)
        self.panel.jog_step(JogAxis.Y, -1.0)
        self.mock_jog.jog.assert_called_once_with('Y', -5.0)
        self.mock_query.query_status.assert_called_once()

    def test_jog_step_string_axis(self) -> None:
        '''
            Tests jog step with string axis identifier.
        '''
        self.panel.jog_step('Z', 1.0)
        self.mock_jog.jog.assert_called_once_with('Z', 10.0)
        self.mock_query.query_status.assert_called_once()


if __name__ == '__main__':
    main()
