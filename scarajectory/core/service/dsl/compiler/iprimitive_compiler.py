# -*- coding: UTF-8 -*-

'''
Module
    iprimitive_compiler.py
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
    Defines structural runtime-checkable protocol IPrimitiveCompiler for processing primitive DSL instructions.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.ast.iscara_instruction import IScaraInstruction
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.scara_compiler_context import (
    ScaraCompilerContext,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPrimitiveCompiler(Protocol):
    '''
        Structural protocol defining contracts for primitive instruction compilation.

        It defines:

            :methods:
                | can_compile - Checks if compiler handles given instruction command type.
                | compile - Compiles instruction, updating context and accumulator waypoints.
    '''

    def can_compile(self, *, instruction: IScaraInstruction) -> bool:
        '''
            Determines whether this sub-compiler handles the specified instruction.

            :param instruction: Primitive AST instruction node.
            :return: True if this compiler handles the instruction, False otherwise.
        '''

    def compile(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Processes the instruction, updating compiler state context or appending waypoints.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
        '''
