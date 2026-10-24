# -*- coding: UTF-8 -*-

'''
Module
    parameter_test.py
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
    Unit tests for ParameterSection component.
'''

from __future__ import annotations

from tkinter import Tk
from tkinter.ttk import Spinbox
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.section.parameter import ParameterSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ParameterSectionTestCase(TestCase):
    '''
        Test cases verifying toolbar parameter inputs and limits.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | setUp - Sets up mock canvas and parameter section.
                | tearDown - Tears down parameter section widget.
                | test_set_deadzone - Tests updating deadzone enforcement state.
                | test_on_defaults_changed - Tests updating settings on canvas and graceful fallback.
    '''

    root: Tk

    @classmethod
    def setUpClass(cls) -> None:
        '''
            Sets up root Tk fixture.

            :exceptions: None.
        '''
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls) -> None:
        '''
            Tears down root Tk fixture.

            :exceptions: None.
        '''
        cls.root.destroy()

    def setUp(self) -> None:
        '''
            Sets up mock canvas and parameter section.

            :exceptions: None.
        '''
        self.mock_canvas = MagicMock(spec=ICanvas)
        self.settings = CanvasSettings(
            default_z=15.0, default_speed=40.0, enforce_deadzone=True
        )
        self.section = ParameterSection(
            self.root,
            canvas=self.mock_canvas,
            reach_limits=(50.0, 200.0),
            settings=self.settings,
        )

    def tearDown(self) -> None:
        '''
            Tears down parameter section widget.

            :exceptions: None.
        '''
        self.section.destroy()

    def test_set_deadzone(self) -> None:
        '''
            Tests updating deadzone enforcement state.

            :exceptions: None.
        '''
        self.section.set_deadzone(False)
        self.mock_canvas.update_settings.assert_called()
        last_settings: CanvasSettings = (
            self.mock_canvas.update_settings.call_args[0][0]
        )
        self.assertFalse(last_settings.enforce_deadzone)

    def test_on_defaults_changed(self) -> None:
        '''
            Tests updating settings on canvas and graceful fallback.

            :exceptions: None.
        '''
        spinboxes = [
            w for w in self.section.winfo_children() if isinstance(w, Spinbox)
        ]
        self.assertEqual(len(spinboxes), 2)
        spinboxes[0].set('30.0')
        spinboxes[1].set('60.0')
        self.section.on_defaults_changed()

        self.mock_canvas.update_settings.assert_called()
        last_settings: CanvasSettings = (
            self.mock_canvas.update_settings.call_args[0][0]
        )
        self.assertEqual(last_settings.default_z, 30.0)
        self.assertEqual(last_settings.default_speed, 60.0)

        spinboxes[0].set('invalid')
        self.section.on_defaults_changed()


if __name__ == '__main__':
    main()
