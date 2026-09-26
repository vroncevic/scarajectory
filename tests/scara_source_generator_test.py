# -*- coding: UTF-8 -*-

'''
Module
    scara_source_generator_test.py
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
    Unit tests for ScaraSourceGenerator.
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
from scarajectory.core.service.dsl.ast.scara_source_generator import ScaraSourceGenerator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraSourceGeneratorTest(TestCase):
    '''Unit tests validating ScaraSourceGenerator DSL source code unparsing.'''

    def test_generate_source_empty(self) -> None:
        '''Verify that an empty program produces an empty string.'''
        program = Program(instructions=())
        source = ScaraSourceGenerator.generate_source(program=program)
        self.assertEqual(source, '')

    def test_generate_source_multiple_instructions(self) -> None:
        '''Verify source text unparsing with newline termination.'''
        inst1 = Instruction(
            command_type=CommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        inst2 = Instruction(
            command_type=CommandType.MOVE_L,
            line_number=2,
            raw_text='MOVE_L X=100.0 Y=150.0',
            parameters={'X': 100.0, 'Y': 150.0},
        )
        program = Program(instructions=(inst1, inst2))
        source = ScaraSourceGenerator.generate_source(program=program)
        self.assertEqual(source, 'HOME\nMOVE_L X=100.0 Y=150.0')


if __name__ == '__main__':
    main()
