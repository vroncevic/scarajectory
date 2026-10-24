# -*- coding: UTF-8 -*-

'''
Module
    actuator_test.py
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
    Unit tests for ActuatorSection component.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Button
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.override.actuator import ActuatorSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestActuatorSection(TestCase):
    '''
        Tests ActuatorSection component and action dispatches.
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
        self.mock_delegate = MagicMock()
        self.section = ActuatorSection(
            self.root,
            action_delegate=self.mock_delegate,
        )

    def tearDown(self) -> None:
        self.section.destroy()

    def test_actions(self) -> None:
        '''
            Tests button action delegate dispatching.

            :exceptions: None.
        '''
        self.mock_delegate.on_toggle_pump.return_value = True
        self.section.on_home_robot()
        self.mock_delegate.on_home_robot.assert_called_once()

        self.section.on_toggle_pump()
        self.mock_delegate.on_toggle_pump.assert_called_once()
        buttons = [w for w in self.section.winfo_children() if isinstance(w, Button)]
        self.assertEqual(buttons[1].cget('text'), 'Pump: ON')

        self.section.on_purge_valve()
        self.mock_delegate.on_purge_valve.assert_called_once()

    def test_set_pump_active(self) -> None:
        '''
            Tests pump active state button text updates.

            :exceptions: None.
        '''
        buttons = [w for w in self.section.winfo_children() if isinstance(w, Button)]
        self.section.set_pump_active(True)
        self.assertEqual(buttons[1].cget('text'), 'Pump: ON')

        self.section.set_pump_active(False)
        self.assertEqual(buttons[1].cget('text'), 'Pump: OFF')


if __name__ == '__main__':
    main()
