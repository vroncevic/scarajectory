# -*- coding: UTF-8 -*-

'''
Module
    toolbar_test.py
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
    Unit tests for Toolbar and ToolbarFactory.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.itoolbar import IToolbar
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar
from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.toolbar_factory import ToolbarFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestToolbar(TestCase):
    '''
        Test cases verifying Toolbar orchestration and decomposed components.
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
        self.mock_navigator = MagicMock()
        self.mock_status_presenter = MagicMock()
        self.mock_history = MagicMock()
        self.settings = CanvasSettings(
            default_z=20.0, default_speed=50.0, enforce_deadzone=True
        )
        bundle = ToolbarBundle(
            canvas=self.mock_canvas,
            navigator=self.mock_navigator,
            status_presenter=self.mock_status_presenter,
            history=self.mock_history,
            r_min=60.0,
            r_max=220.0,
            settings=self.settings,
        )
        self.toolbar: Toolbar = ToolbarFactory.create(self.root, bundle)

    def tearDown(self) -> None:
        self.toolbar.destroy()

    def test_factory_get_version(self) -> None:
        '''
            Tests ToolbarFactory version retrieval.
        '''
        self.assertEqual(ToolbarFactory.get_version(), '1.0.4')

    def test_protocol_conformance(self) -> None:
        '''
            Tests that Toolbar conforms to IToolbar structural protocol.
        '''
        self.assertIsInstance(self.toolbar, IToolbar)

    def test_mounted_subcomponents(self) -> None:
        '''
            Tests that decomposed subcomponents are mounted.
        '''
        self.assertIsNotNone(self.toolbar._tool_selector)
        self.assertIsNotNone(self.toolbar._nav_controls)
        self.assertIsNotNone(self.toolbar._param_inputs)

    def test_get_cursor_label_delegation(self) -> None:
        '''
            Tests cursor label retrieval delegation.
        '''
        lbl = self.toolbar.get_cursor_label()
        self.assertIsNotNone(lbl)
        self.assertEqual(lbl, self.toolbar._param_inputs.get_cursor_label())

    def test_set_deadzone_delegation(self) -> None:
        '''
            Tests deadzone setting delegation.
        '''
        self.toolbar.set_deadzone(False)
        self.assertFalse(self.toolbar._param_inputs._deadzone_var.get())


if __name__ == '__main__':
    main()
