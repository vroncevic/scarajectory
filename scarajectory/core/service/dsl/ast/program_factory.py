# -*- coding: UTF-8 -*-

'''
Module
    program_factory.py
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
    Factory service for creating immutable Program AST root entities with explicit arguments.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.ast.program import Program

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProgramFactory:
    '''
        Domain service providing factory creation for Program AST root entities.

        It defines:

            :methods:
                | create - Creates an immutable Program from a sequence of instructions.
    '''

    @classmethod
    def create(cls, *, instructions: Sequence[Instruction]) -> Program:
        '''
            Constructs an immutable Program instance from an instruction sequence.

            :param instructions: Sequence of Instruction instances.
            :return: Immutable Program instance.
        '''
        return Program(instructions=tuple(instructions))

    @classmethod
    def from_instructions(cls, *, instructions: Sequence[Instruction]) -> Program:
        '''
            Constructs an immutable Program from an instruction sequence.

            :param instructions: Sequence of Instruction instances.
            :return: Immutable Program instance.
        '''
        return cls.create(instructions=instructions)

