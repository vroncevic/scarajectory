# -*- coding: UTF-8 -*-

'''
Module
    imacro_expander.py
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
    Defines structural runtime-checkable protocol IMacroExpander for domain macro expansion.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.iscara_instruction import IScaraInstruction
from scarajectory.core.service.dsl.scara_compiler_context import ScaraCompilerContext

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMacroExpander(Protocol):
    '''
        Structural protocol defining contract for expanding high-level SCARA macros into primitives.

        It defines:

            :attributes:
                | None.
            :methods:
                | can_expand - Checks if macro expander applies to given instruction node.
                | expand - Expands macro instruction into tuple of lower-level primitive instructions.
    '''

    def can_expand(self, *, instruction: IScaraInstruction) -> bool:
        '''
            Checks whether this expander handles the given instruction type.

            :param instruction: Instruction node to check.
            :return: True if expander can handle the instruction, False otherwise.
        '''
        ...

    def expand(
        self,
        *,
        instruction: IScaraInstruction,
        context: ScaraCompilerContext,
    ) -> tuple[IScaraInstruction, ...]:
        '''
            Expands macro instruction into one or more primitive instructions.

            :param instruction: Macro instruction to expand.
            :param context: Stateful compilation context.
            :return: Tuple of expanded primitive IScaraInstruction nodes.
        '''
        ...
