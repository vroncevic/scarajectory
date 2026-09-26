# -*- coding: UTF-8 -*-

'''
Module
    motion_command_compiler.py
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
    Coordinates compilation of Cartesian linear, joint, approach, retract, and arc motion DSL instructions.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.primitive.iprimitive_compiler import IPrimitiveCompiler
from scarajectory.core.service.dsl.compiler.scara_compiler_context import ScaraCompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandCompiler:
    '''
        Sub-compiler coordinator handling motion instructions (MOVE_L, MOVE_J, APPROACH, RETRACT, ARC_CW, ARC_CCW).
        Delegates compilation directly to specialized sub-compilers without private methods.

        It defines:

            :attributes:
                | _SUPPORTED - Frozenset of handled CommandType instances.
                | _cartesian_compiler - Sub-compiler for Cartesian linear and joint moves.
                | _vertical_compiler - Sub-compiler for approach and retract moves.
                | _arc_compiler - Sub-compiler for circular arc moves.
            :methods:
                | __init__ - Initializes motion compiler with injected sub-compilers.
                | can_compile - Checks if command is a motion instruction.
                | compile - Delegates compilation to matching sub-compiler.
    '''

    _SUPPORTED: frozenset[CommandType] = frozenset({
        CommandType.MOVE_L,
        CommandType.MOVE_J,
        CommandType.APPROACH,
        CommandType.RETRACT,
        CommandType.ARC_CW,
        CommandType.ARC_CCW,
    })

    _cartesian_compiler: IPrimitiveCompiler
    _vertical_compiler: IPrimitiveCompiler
    _arc_compiler: IPrimitiveCompiler

    def __init__(
        self,
        *,
        cartesian_compiler: IPrimitiveCompiler,
        vertical_compiler: IPrimitiveCompiler,
        arc_compiler: IPrimitiveCompiler,
    ) -> None:
        '''
            Initializes MotionCommandCompiler with injected sub-compilers.

            :param cartesian_compiler: Injected sub-compiler for Cartesian moves.
            :param vertical_compiler: Injected sub-compiler for vertical moves.
            :param arc_compiler: Injected sub-compiler for circular arcs.
            :exceptions: None.
        '''
        self._cartesian_compiler = cartesian_compiler
        self._vertical_compiler = vertical_compiler
        self._arc_compiler = arc_compiler

    def can_compile(self, *, instruction: Instruction) -> bool:
        '''
            Determines whether this coordinator handles the specified instruction.

            :param instruction: Primitive AST instruction node.
            :return: True if handled, False otherwise.
            :exceptions: None.
        '''
        return instruction.command_type in self._SUPPORTED

    def compile(
        self,
        *,
        instruction: Instruction,
        context: ScaraCompilerContext,
        waypoints: list[Waypoint],
    ) -> None:
        '''
            Processes motion instructions by delegating to the appropriate sub-compiler.

            :param instruction: Primitive AST instruction node.
            :param context: Mutable compiler execution context.
            :param waypoints: Accumulator list of compiled Waypoint instances.
            :exceptions: None.
        '''
        if self._cartesian_compiler.can_compile(instruction=instruction):
            self._cartesian_compiler.compile(
                instruction=instruction,
                context=context,
                waypoints=waypoints,
            )
        elif self._vertical_compiler.can_compile(instruction=instruction):
            self._vertical_compiler.compile(
                instruction=instruction,
                context=context,
                waypoints=waypoints,
            )
        elif self._arc_compiler.can_compile(instruction=instruction):
            self._arc_compiler.compile(
                instruction=instruction,
                context=context,
                waypoints=waypoints,
            )
