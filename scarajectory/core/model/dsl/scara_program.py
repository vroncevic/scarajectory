# -*- coding: UTF-8 -*-

'''
Module
    scara_program.py
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
    Defines immutable ScaraProgram AST root containing sequence of parsed instructions.
'''

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraProgram:
    '''
        Immutable AST root entity representing a complete parsed SCARA DSL program.

        It defines:

            :attributes:
                | instructions - Immutable tuple of instruction nodes.
            :methods:
                | instruction_count - Property returning total instruction count.
                | to_text - Serializes program back into formatted source text.
                | to_dict - Serializes program to dictionary.
                | from_instructions - Factory method creating program from an instruction sequence.
    '''

    instructions: tuple[IScaraInstruction, ...] = field(default_factory=tuple)

    @classmethod
    def from_instructions(
        cls, instructions: Sequence[IScaraInstruction]
    ) -> ScaraProgram:
        '''
            Factory constructor creating ScaraProgram from an arbitrary sequence of instructions.

            :param instructions: Sequence of instruction instances.
            :return: New immutable ScaraProgram instance.
        '''
        return cls(instructions=tuple(instructions))

    @property
    def instruction_count(self) -> int:
        '''
            Property returning number of executable instructions.

            :return: Instruction count integer.
        '''
        return len(self.instructions)

    def to_text(self) -> str:
        '''
            Serializes program back into standard .scara DSL source text.

            :return: Formatted text string.
        '''
        lines: list[str] = []
        for inst in self.instructions:
            if inst.raw_text:
                lines.append(inst.raw_text)
            else:
                params_str = ' '.join(
                    f'{k}={v}' for k, v in inst.parameters.items()
                )
                lines.append(f'{inst.command_type.value} {params_str}'.strip())
        return '\n'.join(lines)

    def to_dict(self) -> dict[str, Any]:
        '''
            Serializes program to dictionary representation.

            :return: Dictionary representation of program.
        '''
        return {
            'instruction_count': len(self.instructions),
            'instructions': [inst.to_dict() for inst in self.instructions],
        }
