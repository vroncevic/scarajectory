# -*- coding: UTF-8 -*-

'''
Module
    jog_power_panel_test.py
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
    Unit tests for JogPowerPanel and JogPowerPanelFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.jog.power_panel import JogPowerPanel
from scarajectory.infrastructure.gui.manipulator.jog.power_panel_factory import JogPowerPanelFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestJogPowerPanel(TestCase):
    '''
        Test cases verifying JogPowerPanel action dispatching and factory.
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
        self.mock_motion = MagicMock()
        self.panel: JogPowerPanel = JogPowerPanelFactory.create(
            self.root,
            motion_controller=self.mock_motion,
        )

    def tearDown(self) -> None:
        self.panel.destroy()

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.
        '''
        self.assertEqual(JogPowerPanelFactory.get_version(), '1.0.4')

    def test_enable(self) -> None:
        '''
            Tests that enable commands the motion controller.
        '''
        self.panel.enable()
        self.mock_motion.enable.assert_called_once()

    def test_disable(self) -> None:
        '''
            Tests that disable commands the motion controller.
        '''
        self.panel.disable()
        self.mock_motion.disable.assert_called_once()

    def test_home(self) -> None:
        '''
            Tests that home commands the motion controller.
        '''
        self.panel.home()
        self.mock_motion.home.assert_called_once()


if __name__ == '__main__':
    main()
