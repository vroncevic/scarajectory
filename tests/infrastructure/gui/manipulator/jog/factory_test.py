# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for JogTabFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.jog.dependencies import JogDependencies
from scarajectory.infrastructure.gui.manipulator.jog.factory import JogTabFactory
from scarajectory.infrastructure.gui.manipulator.jog.tab import JogTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogTabFactory(TestCase):
    '''
        Test cases verifying JogTabFactory instantiation and versioning.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.root.destroy()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        self.assertEqual(JogTabFactory.get_version(), '1.0.3')

    def test_create(self) -> None:
        '''
            Tests creating assembled JogTab instance with factory.

            :exceptions: None.
        '''
        deps = JogDependencies(
            raw_channel=MagicMock(),
            motion_controller=MagicMock(),
            jog_controller=MagicMock(),
            tool_controller=MagicMock(),
            query_controller=MagicMock(),
        )
        tab: JogTab = JogTabFactory.create(self.root, dependencies=deps)
        self.assertIsInstance(tab, JogTab)
        self.assertIsNotNone(tab.panels.power_panel)
        self.assertIsNotNone(tab.panels.axis_grid_panel)
        self.assertIsNotNone(tab.panels.tool_panel)
        self.assertIsNotNone(tab.panels.raw_panel)
        tab.destroy()


if __name__ == '__main__':
    main()
