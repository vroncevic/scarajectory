# -*- coding: UTF-8 -*-

'''
Module
    instruction_factory_test.py
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
    Unit tests for InstructionFactory.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from types import MappingProxyType
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.dsl.ast.command_type import CommandType
from scarajectory.core.service.dsl.ast.instruction_factory import InstructionFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class InstructionFactoryTest(TestCase):
    '''Unit tests validating factory instantiation and default assignment of Instruction.'''

    def test_create_with_defaults(self) -> None:
        '''Verify creating an instruction without parameters defaults to empty MappingProxyType.'''
        instruction = InstructionFactory.create(
            command_type=CommandType.HOME,
            line_number=1,
            raw_text='HOME',
            parameters={},
        )
        self.assertEqual(instruction.command_type, CommandType.HOME)
        self.assertEqual(instruction.line_number, 1)
        self.assertEqual(instruction.raw_text, 'HOME')
        self.assertEqual(len(instruction.parameters), 0)
        self.assertIsInstance(instruction.parameters, MappingProxyType)

    def test_create_with_parameters(self) -> None:
        '''Verify creating an instruction with parameters dictionary.'''
        instruction = InstructionFactory.create(
            command_type=CommandType.MOVE_L,
            line_number=10,
            raw_text='MOVE_L X=10.0 Y=20.0',
            parameters={'X': 10.0, 'Y': 20.0},
        )
        self.assertEqual(instruction.command_type, CommandType.MOVE_L)
        self.assertEqual(instruction.line_number, 10)
        self.assertEqual(instruction.parameters['X'], 10.0)
        self.assertEqual(instruction.parameters['Y'], 20.0)
        self.assertIsInstance(instruction.parameters, MappingProxyType)


if __name__ == '__main__':
    main()
