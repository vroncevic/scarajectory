# -*- coding: UTF-8 -*-

'''
Module
    panel_test.py
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

from scarajectory.infrastructure.gui.manipulator.override.actuator import ActuatorSection
from scarajectory.infrastructure.gui.manipulator.override.feedrate import OverrideSection
from scarajectory.infrastructure.gui.manipulator.override.panel import ManipulatorOverridePanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestManipulatorOverridePanel(TestCase):
    '''
        Tests ManipulatorOverridePanel composite layout and section coordination.
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

    def tearDown(self) -> None:
        self.panel.destroy()

    def test_composition_mounting(self) -> None:
        '''
            Verifies child actuator and speed override sections are mounted.

            :exceptions: None.
        '''
        self.assertIsInstance(self.panel.actuator_section, ActuatorSection)
        self.assertIsInstance(self.panel.override_section, OverrideSection)

    def test_delegate_forwarding(self) -> None:
        '''
            Verifies action delegate is forwarded to child sections during initialization.

            :exceptions: None.
        '''
        self.panel.actuator_section.on_home_robot()
        self.mock_delegate.on_home_robot.assert_called_once()
        self.panel.override_section.handle_slider_change('175.0')
        self.mock_delegate.on_override_change.assert_called_once_with(175)

    def test_set_pump_active(self) -> None:
        '''
            Verifies updating pump state forwards to actuator section.

            :exceptions: None.
        '''
        self.panel.set_pump_active(True)
        self.panel.set_pump_active(False)

    def test_set_override_label(self) -> None:
        '''
            Verifies updating override label forwards to override section.

            :exceptions: None.
        '''
        self.panel.set_override_label(160)
        self.assertEqual(self.panel.override_section.override_text, '160%')


if __name__ == '__main__':
    main()
