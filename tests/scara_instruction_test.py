# -*- coding: UTF-8 -*-

'''
Module
    scara_instruction_test.py
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
    Unit tests for Instruction AST model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from sys import path
from types import MappingProxyType
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

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


class ScaraInstructionTest(TestCase):
    '''Unit tests validating Instruction AST node immutability and attributes.'''

    def test_instantiation_and_attributes(self) -> None:
        '''Verify proper attribute initialization and mapping encapsulation.'''
        instruction = Instruction(
            command_type=CommandType.MOVE_L,
            line_number=42,
            raw_text='MOVE_L X=100.0 Y=200.0 Z=10.0',
            parameters=MappingProxyType({'X': 100.0, 'Y': 200.0, 'Z': 10.0}),
        )
        self.assertEqual(instruction.command_type, CommandType.MOVE_L)
        self.assertEqual(instruction.line_number, 42)
        self.assertEqual(instruction.raw_text, 'MOVE_L X=100.0 Y=200.0 Z=10.0')
        self.assertEqual(instruction.parameters['X'], 100.0)
        self.assertEqual(instruction.parameters['Y'], 200.0)
        self.assertEqual(instruction.parameters['Z'], 10.0)
        self.assertIsInstance(instruction.parameters, MappingProxyType)

    def test_frozen_immutability(self) -> None:
        '''Verify that modifying attributes raises FrozenInstanceError.'''
        instruction = Instruction(
            command_type=CommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters=MappingProxyType({}),
        )
        with self.assertRaises(FrozenInstanceError):
            instruction.line_number = 2  # type: ignore[misc]

    def test_parameters_mutation_rejected(self) -> None:
        '''Verify that mutating the parameters proxy raises TypeError.'''
        raw_dict = {'SPEED': 50.0}
        instruction = Instruction(
            command_type=CommandType.SPEED,
            line_number=5,
            raw_text='SPEED 50',
            parameters=MappingProxyType(raw_dict),
        )
        with self.assertRaises(TypeError):
            instruction.parameters['SPEED'] = 100.0  # type: ignore[index]


if __name__ == '__main__':
    main()
