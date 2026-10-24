# -*- coding: UTF-8 -*-

'''
Module
    feedrate_test.py
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
    Unit tests for OverrideSection component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.manipulator.override.feedrate import OverrideSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestOverrideSection(TestCase):
    '''
        Tests OverrideSection component and speed override dispatches.
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
        self.section = OverrideSection(
            self.root,
            action_delegate=self.mock_delegate,
        )

    def tearDown(self) -> None:
        self.section.destroy()

    def test_slider_change(self) -> None:
        '''
            Tests slider movement dispatching.

            :exceptions: None.
        '''
        self.section.handle_slider_change('150.0')
        self.mock_delegate.on_override_change.assert_called_once_with(150)
        self.assertEqual(self.section.override_text, '150%')

    def test_slider_clamping(self) -> None:
        '''
            Tests clamping to allowable percentage boundaries.

            :exceptions: None.
        '''
        self.section.handle_slider_change('5.0')
        self.assertEqual(self.section.override_text, '10%')

        self.section.handle_slider_change('250.0')
        self.assertEqual(self.section.override_text, '200%')

    def test_set_override_label(self) -> None:
        '''
            Tests directly updating override percentage label.

            :exceptions: None.
        '''
        self.section.set_override_label(120)
        self.assertEqual(self.section.override_text, '120%')


if __name__ == '__main__':
    main()
