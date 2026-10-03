# -*- coding: UTF-8 -*-

'''
Module
    iexecution_delegate.py
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
    Defines structural protocol IDslExecutionDelegate for DSL compilation and validation actions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IDslExecutionDelegate(Protocol):
    '''
        Structural protocol defining DSL compilation, validation, and preview actions.

        It defines:

            :methods:
                | compile_to_plan - Compiles DSL code to active trajectory plan.
                | validate_code - Runs syntax and reachability validation on editor code.
                | export_plan_to_editor - Serializes current active plan into DSL code.
                | preview_in_scaraemu - Launches SCARAEmu emulator preview.
    '''

    def compile_to_plan(self) -> None:
        '''
            Compiles DSL code to active trajectory plan.
        '''

    def validate_code(self) -> None:
        '''
            Runs syntax and reachability validation on editor code.
        '''

    def export_plan_to_editor(self) -> None:
        '''
            Serializes current active plan into DSL code.
        '''

    def preview_in_scaraemu(self) -> None:
        '''
            Launches SCARAEmu emulator preview.
        '''
