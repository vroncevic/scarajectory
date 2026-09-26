# -*- coding: UTF-8 -*-

'''
Module
    scara_source_generator.py
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
    Service providing source code unparsing and text generation from SCARA AST programs.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.ast.program import Program

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraSourceGenerator:
    '''
        Domain service for unparsing Program AST structures back into DSL source text.

        It defines:

            :methods:
                | generate_source - Reconstructs .scara source code string from AST.
    '''

    @classmethod
    def generate_source(cls, *, program: Program) -> str:
        '''
            Serializes a Program back into standard .scara DSL source text.

            :param program: Program AST root.
            :return: Formatted source text string.
        '''
        lines: list[str] = []

        for inst in program.instructions:
            if inst.raw_text:
                lines.append(inst.raw_text)
            else:
                params_str: str = ' '.join(
                    f'{k}={v}' for k, v in inst.parameters.items()
                )
                lines.append(f'{inst.command_type.value} {params_str}'.strip())

        return '\n'.join(lines)
