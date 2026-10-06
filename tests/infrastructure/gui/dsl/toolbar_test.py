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
    Unit tests for DslEditorToolbar component.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.gui.dsl.toolbar import DslEditorToolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestDslEditorToolbar(TestCase):
    '''
        Test cases verifying DslEditorToolbar layout and delegation behavior.
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
        self.mock_execution = MagicMock()
        self.mock_file = MagicMock()
        self.mock_binary = MagicMock()

        self.toolbar: DslEditorToolbar = DslEditorToolbar(
            self.root,
            execution_delegate=self.mock_execution,
            file_delegate=self.mock_file,
            binary_delegate=self.mock_binary,
        )

    def tearDown(self) -> None:
        self.toolbar.destroy()

    def test_example_selection(self) -> None:
        '''
            Tests setting and getting selected example filename.
        '''
        self.toolbar.set_selected_example('custom_script.scara')
        self.assertEqual(self.toolbar.get_selected_example(), 'custom_script.scara')

    def test_set_example_files_with_industrial_pick_place(self) -> None:
        '''
            Tests set_example_files defaults to 12_industrial_pick_place.scara when present.
        '''
        files = ['01_linear.scara', '12_industrial_pick_place.scara', '05_circle.scara']
        self.toolbar.set_example_files(files)
        self.assertEqual(self.toolbar.get_selected_example(), '12_industrial_pick_place.scara')

    def test_set_example_files_fallback_to_first(self) -> None:
        '''
            Tests set_example_files defaults to first entry when default is not present.
        '''
        files = ['01_linear.scara', '05_circle.scara']
        self.toolbar.set_example_files(files)
        self.assertEqual(self.toolbar.get_selected_example(), '01_linear.scara')

    def test_handle_example_change(self) -> None:
        '''
            Tests handle_example_change forwards selected example to file delegate.
        '''
        self.toolbar.set_selected_example('test.scara')
        self.toolbar.handle_example_change()
        self.mock_file.on_example_selected.assert_called_once_with('test.scara')


if __name__ == '__main__':
    main()
