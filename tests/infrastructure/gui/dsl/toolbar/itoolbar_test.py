# -*- coding: UTF-8 -*-

'''
Module
    itoolbar_test.py
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
    Unit tests for IDslEditorToolbar structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.toolbar.itoolbar import IDslEditorToolbar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidToolbarMock:
    '''
        Mock conforming structurally to IDslEditorToolbar.
    '''

    def handle_example_change(self, _event: object = '') -> None:
        '''
            Handles example change.
        '''

    def get_selected_example(self) -> str:
        '''
            Gets selected example.
        '''
        return 'test.scara'

    def set_selected_example(self, name: str) -> None:
        '''
            Sets selected example.
        '''

    def set_example_files(self, files: list[str]) -> None:
        '''
            Sets example files.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.
        '''
        return '1.0.3'


class IncompleteToolbarMock:
    '''
        Mock missing required protocol methods.
    '''

    def get_selected_example(self) -> str:
        '''
            Returns dummy example name.
        '''
        return 'test.scara'

    def get_name(self) -> str:
        '''
            Returns dummy name to satisfy public methods minimum.
        '''
        return 'incomplete'


class TestIDslEditorToolbar(TestCase):
    '''
        Tests verifying runtime checkable compliance for IDslEditorToolbar.
    '''

    def test_valid_implementation_is_instance(self) -> None:
        '''
            Verifies that a valid structural mock satisfies IDslEditorToolbar.

            :exceptions: None.
        '''
        mock = ValidToolbarMock()
        self.assertTrue(isinstance(mock, IDslEditorToolbar))

    def test_incomplete_implementation_fails(self) -> None:
        '''
            Verifies that an incomplete mock fails IDslEditorToolbar protocol check.

            :exceptions: None.
        '''
        mock = IncompleteToolbarMock()
        self.assertFalse(isinstance(mock, IDslEditorToolbar))


if __name__ == '__main__':
    main()
