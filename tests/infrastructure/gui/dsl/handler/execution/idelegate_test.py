# -*- coding: UTF-8 -*-

'''
Module
    idelegate_test.py
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
    Unit tests for IDslExecutionDelegate structural protocol contract.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.infrastructure.gui.dsl.handler.execution.idelegate import IDslExecutionDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidExecutionDelegateMock:
    '''
        Mock conforming structurally to IDslExecutionDelegate.
    '''

    def compile_to_plan(self) -> None:
        '''
            Compiles to plan.
        '''

    def validate_code(self) -> None:
        '''
            Validates code.
        '''

    def export_plan_to_editor(self) -> None:
        '''
            Exports plan to editor.
        '''

    def preview_in_scaraemu(self) -> None:
        '''
            Previews in SCARAEmu.
        '''

    def get_version(self) -> str:
        '''
            Returns version string.
        '''
        return '1.0.3'


class IncompleteExecutionDelegateMock:
    '''
        Mock missing required protocol methods.
    '''

    def compile_to_plan(self) -> None:
        '''
            Compiles to plan.
        '''

    def get_name(self) -> str:
        '''
            Returns dummy name to satisfy public methods minimum.
        '''
        return 'incomplete'


class TestIDslExecutionDelegate(TestCase):
    '''
        Tests verifying runtime checkable compliance for IDslExecutionDelegate.
    '''

    def test_valid_implementation_is_instance(self) -> None:
        '''
            Verifies that a valid structural mock satisfies IDslExecutionDelegate.

            :exceptions: None.
        '''
        mock = ValidExecutionDelegateMock()
        self.assertTrue(isinstance(mock, IDslExecutionDelegate))

    def test_incomplete_implementation_fails(self) -> None:
        '''
            Verifies that an incomplete mock fails IDslExecutionDelegate check.

            :exceptions: None.
        '''
        mock = IncompleteExecutionDelegateMock()
        self.assertFalse(isinstance(mock, IDslExecutionDelegate))


if __name__ == '__main__':
    main()
