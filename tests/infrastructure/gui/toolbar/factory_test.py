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
    Unit tests for ToolbarFactory component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.factory import ToolbarFactory
from scarajectory.infrastructure.gui.toolbar.toolbar import Toolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarFactoryTestCase(TestCase):
    '''
        Test cases verifying ToolbarFactory assembly behavior.

        It defines:

            :methods:
                | setUpClass - Sets up root Tk fixture.
                | tearDownClass - Tears down root Tk fixture.
                | test_factory_version - Tests factory version string.
                | test_create_toolbar - Tests assembling Toolbar via factory.
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

    def test_factory_version(self) -> None:
        '''
            Tests factory version string.

            :exceptions: None.
        '''
        self.assertEqual(ToolbarFactory.get_version(), '1.0.3')

    def test_create_toolbar(self) -> None:
        '''
            Tests assembling Toolbar via factory.

            :exceptions: None.
        '''
        bundle = ToolbarBundle(
            canvas=MagicMock(),
            navigator=MagicMock(),
            status_presenter=MagicMock(),
            history=MagicMock(),
            r_min=60.0,
            r_max=220.0,
            settings=CanvasSettings(
                default_z=20.0, default_speed=50.0, enforce_deadzone=True
            ),
        )
        toolbar: Toolbar = ToolbarFactory.create(self.root, bundle)
        self.assertIsInstance(toolbar, Toolbar)
        toolbar.destroy()


if __name__ == '__main__':
    main()
