# -*- coding: UTF-8 -*-

'''
Module
    toolbar_parameter_inputs_test.py
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
    Unit tests for ToolbarParameterInputs and its factory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.parameter_inputs import ToolbarParameterInputs
from scarajectory.infrastructure.gui.toolbar.parameter_inputs_bundle import ParameterInputsBundle
from scarajectory.infrastructure.gui.toolbar.parameter_inputs_factory import ToolbarParameterInputsFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolbarParameterInputs(TestCase):
    '''
        Test cases verifying toolbar parameter inputs and cursor monitor.
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
        self.mock_canvas = MagicMock()
        self.mock_status_presenter = MagicMock()
        self.settings = CanvasSettings(
            default_z=15.0, default_speed=40.0, enforce_deadzone=True
        )
        self.bundle = ParameterInputsBundle(
            canvas=self.mock_canvas,
            status_presenter=self.mock_status_presenter,
            r_min=50.0,
            r_max=200.0,
            settings=self.settings,
        )
        self.inputs: ToolbarParameterInputs = (
            ToolbarParameterInputsFactory.create(self.root, self.bundle)
        )

    def tearDown(self) -> None:
        self.inputs.destroy()

    def test_cursor_label_registered(self) -> None:
        '''
            Tests cursor label widget is registered with status presenter.
        '''
        lbl = self.inputs.get_cursor_label()
        self.assertIsNotNone(lbl)
        self.mock_status_presenter.set_hover_label.assert_called_once_with(lbl)

    def test_set_deadzone(self) -> None:
        '''
            Tests updating deadzone enforcement state.
        '''
        self.inputs.set_deadzone(False)
        self.assertFalse(self.inputs._deadzone_var.get())
        self.mock_canvas.update_settings.assert_called()

    def test_on_defaults_changed(self) -> None:
        '''
            Tests on_defaults_changed pushes new CanvasSettings to canvas.
        '''
        self.inputs._spin_z.set('30.0')
        self.inputs._spin_speed.set('60.0')
        self.inputs.on_defaults_changed()

        self.mock_canvas.update_settings.assert_called()
        last_settings: CanvasSettings = (
            self.mock_canvas.update_settings.call_args[0][0]
        )
        self.assertEqual(last_settings.default_z, 30.0)
        self.assertEqual(last_settings.default_speed, 60.0)

    def test_factory_version(self) -> None:
        '''
            Tests factory version retrieval.
        '''
        self.assertEqual(ToolbarParameterInputsFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
