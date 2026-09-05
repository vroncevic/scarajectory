# -*- coding: UTF-8 -*-

'''
Module
    iscara_program.py
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
    Defines structural runtime-checkable protocol IScaraProgram for complete parsed SCARA DSL programs.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol, runtime_checkable

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraProgram(Protocol):
    '''
        Structural protocol defining contract for parsed SCARA DSL program AST root.

        It defines:

            :attributes:
                | None.
            :methods:
                | instructions - Property returning sequence of instructions.
                | instruction_count - Property returning total number of instructions.
                | to_text - Reconstructs program source code string.
                | to_dict - Serializes program structure to dictionary.
    '''

    @property
    def instructions(self) -> Sequence[IScaraInstruction]:
        '''
            Property returning sequence of parsed instructions.

            :return: Sequence of IScaraInstruction instances.
        '''
        ...

    @property
    def instruction_count(self) -> int:
        '''
            Property returning number of executable instructions.

            :return: Instruction count integer.
        '''
        ...

    def to_text(self) -> str:
        '''
            Serializes program back into standard .scara DSL source text.

            :return: Formatted text string.
        '''
        ...

    def to_dict(self) -> dict[str, Any]:
        '''
            Serializes program to dictionary representation.

            :return: Dictionary representation of program.
        '''
        ...
