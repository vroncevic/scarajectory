# -*- coding: UTF-8 -*-

'''
Module
    iscara_instruction.py
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
    Defines structural runtime-checkable protocol IScaraInstruction for SCARA DSL AST instruction nodes.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Protocol, runtime_checkable

from scarajectory.core.model.dsl.scara_command_type import ScaraCommandType

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraInstruction(Protocol):
    '''
        Structural protocol defining contract for SCARA DSL instruction AST nodes.

        It defines:

            :attributes:
                | None.
            :methods:
                | command_type - Property returning command type enumeration value.
                | line_number - Property returning source code line number.
                | raw_text - Property returning original unparsed instruction line.
                | parameters - Property returning read-only dictionary mapping of parameters.
                | to_dict - Serializes instruction node to dictionary.
    '''

    @property
    def command_type(self) -> ScaraCommandType:
        '''
            Property returning instruction command type.

            :return: ScaraCommandType enum member.
        '''

    @property
    def line_number(self) -> int:
        '''
            Property returning 1-indexed source code line number.

            :return: Line number integer.
        '''

    @property
    def raw_text(self) -> str:
        '''
            Property returning raw source line string.

            :return: Original text string.
        '''

    @property
    def parameters(self) -> Mapping[str, Any]:
        '''
            Property returning mapping of parsed instruction parameters.

            :return: Read-only mapping of parameter names to values.
        '''

    def to_dict(self) -> dict[str, Any]:
        '''
            Serializes instruction node to dictionary representation.

            :return: Dictionary representation of the instruction.
        '''
