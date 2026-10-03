# -*- coding: UTF-8 -*-

'''
Module
    manipulator_override_panel_test.py
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
    Unit tests for ManipulatorOverridePanel component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.manipulator_override_panel import ManipulatorOverridePanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorOverridePanelTestCase(TestCase):
    '''
        Tests ManipulatorOverridePanel component and actions.

        It defines:

            :methods:
                | setUpClass - Initializes root Tkinter window.
                | tearDownClass - Destroys root window.
                | setUp - Sets up mock dependencies and panel instance.
                | test_actions - Verifies action delegate command invocations.
                | test_slider_change - Verifies feedrate override change dispatch.
                | test_set_pump_active - Verifies button text updates.
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
        self.panel = ManipulatorOverridePanel(
            self.root,
            action_delegate=self.mock_delegate,
        )

    def test_actions(self) -> None:
        '''Tests button action delegate dispatching.'''
        self.panel.on_home_robot()
        self.mock_delegate.on_home_robot.assert_called_once()

        self.panel.on_toggle_pump()
        self.mock_delegate.on_toggle_pump.assert_called_once()

        self.panel.on_purge_valve()
        self.mock_delegate.on_purge_valve.assert_called_once()

    def test_slider_change(self) -> None:
        '''Tests slider movement dispatching.'''
        self.panel.handle_slider_change('150.0')
        self.mock_delegate.on_override_change.assert_called_once_with(150)
        self.assertEqual(self.panel.override_text, '150%')

    def test_set_pump_active(self) -> None:
        '''Tests pump active state button text updates.'''
        self.panel.set_pump_active(True)
        self.assertEqual(self.panel.pump_button_text, 'Pump: ON')
        self.panel.set_pump_state(False)
        self.assertEqual(self.panel.pump_button_text, 'Pump: OFF')


if __name__ == '__main__':
    main()
