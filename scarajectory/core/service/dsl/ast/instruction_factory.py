# -*- coding: UTF-8 -*-

'''
Module
    instruction_factory.py
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
    Factory service for creating immutable Instruction AST nodes with explicit parameters.
'''

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionFactory:
    '''
        Domain service providing factory creation for Instruction AST nodes.

        It defines:

            :methods:
                | create - Creates an immutable Instruction instance.
    '''

    @classmethod
    def create(
        cls,
        *,
        command_type: CommandType,
        line_number: int,
        raw_text: str,
        parameters: Mapping[str, Any],
    ) -> Instruction:
        '''
            Creates an immutable Instruction instance with defensive immutability.

            :param command_type: CommandType enum identifier.
            :param line_number: Source code 1-indexed line number.
            :param raw_text: Original raw line string.
            :param parameters: Mapping of instruction parameters.
            :return: Immutable Instruction instance.
        '''
        safe_params: Mapping[str, Any] = (
            parameters
            if isinstance(parameters, MappingProxyType)
            else MappingProxyType(dict(parameters))
        )

        return Instruction(
            command_type=command_type,
            line_number=line_number,
            raw_text=raw_text,
            parameters=safe_params,
        )
