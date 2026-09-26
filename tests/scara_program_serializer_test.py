# -*- coding: UTF-8 -*-

'''
Module
    scara_program_serializer_test.py
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
    Unit tests for ScaraProgramSerializer.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.model.dsl.ast.instruction import Instruction
from scarajectory.core.model.dsl.ast.program import Program
from scarajectory.core.service.dsl.ast.scara_program_serializer import ScaraProgramSerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraProgramSerializerTest(TestCase):
    '''Unit tests validating serialization of AST instructions and programs to dictionaries.'''

    def test_serialize_instruction(self) -> None:
        '''Verify serializing a single instruction to dictionary representation.'''
        inst = Instruction(
            command_type=CommandType.MOVE_L,
            line_number=10,
            raw_text='MOVE_L X=15.0 Y=25.0',
            parameters={'X': 15.0, 'Y': 25.0},
        )
        serialized = ScaraProgramSerializer.serialize_instruction(instruction=inst)
        self.assertEqual(
            serialized,
            {
                'command_type': 'MOVE_L',
                'line_number': 10,
                'raw_text': 'MOVE_L X=15.0 Y=25.0',
                'parameters': {'X': 15.0, 'Y': 25.0},
            },
        )

    def test_serialize_program(self) -> None:
        '''Verify serializing a complete program to dictionary representation.'''
        inst = Instruction(
            command_type=CommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        program = Program(instructions=(inst,))
        serialized = ScaraProgramSerializer.serialize_program(program=program)
        self.assertEqual(serialized['instruction_count'], 1)
        self.assertEqual(len(serialized['instructions']), 1)
        self.assertEqual(serialized['instructions'][0]['command_type'], 'HOME')


if __name__ == '__main__':
    main()
