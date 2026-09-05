# -*- coding: UTF-8 -*-

'''
Module
    scara_instruction.py
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
    Defines immutable ScaraInstruction AST node representing a single parsed DSL command.
'''

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any

from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraInstruction:
    '''
        Immutable AST instruction node representing a single parsed SCARA DSL command.

        It defines:

            :attributes:
                | command_type - Enumeration identifier of the command type.
                | line_number - Source code 1-indexed line number.
                | raw_text - Original raw line string.
                | parameters - Immutable mapping of command parameters.
            :methods:
                | to_dict - Serializes instruction node to dictionary.
    '''

    command_type: ScaraCommandType
    line_number: int
    raw_text: str = ''
    parameters: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        '''
            Ensures defensive immutability for the internal parameter dictionary.

            :exceptions: None.
        '''
        if not isinstance(self.parameters, MappingProxyType):
            object.__setattr__(
                self, 'parameters', MappingProxyType(dict(self.parameters))
            )

    def to_dict(self) -> dict[str, Any]:
        '''
            Serializes instruction node to dictionary representation.

            :return: Dictionary representation of the instruction.
        '''
        return {
            'command_type': self.command_type.value,
            'line_number': self.line_number,
            'raw_text': self.raw_text,
            'parameters': dict(self.parameters),
        }
