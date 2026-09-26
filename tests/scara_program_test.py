# -*- coding: UTF-8 -*-

'''
Module
    scara_program_test.py
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
    Unit tests for Program AST model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.dsl.ast.command_type import CommandType
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


class ScaraProgramTest(TestCase):
    '''Unit tests validating Program purity, immutability and instruction count.'''

    def test_instantiation_and_instructions(self) -> None:
        '''Verify instructions tuple encapsulation.'''
        inst1 = Instruction(
            command_type=CommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        inst2 = Instruction(
            command_type=CommandType.SPEED,
            line_number=2,
            raw_text='SPEED 50',
            parameters={'speed': 50.0},
        )
        program = Program(instructions=(inst1, inst2))
        self.assertEqual(len(program.instructions), 2)
        self.assertEqual(program.instructions[0], inst1)
        self.assertEqual(program.instructions[1], inst2)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying instructions raises FrozenInstanceError.'''
        program = Program(instructions=())
        with self.assertRaises(FrozenInstanceError):
            program.instructions = ()  # type: ignore[misc]


if __name__ == '__main__':
    main()
