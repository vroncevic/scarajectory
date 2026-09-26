# -*- coding: UTF-8 -*-

'''
Module
    icompiler.py
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
    Defines ICompiler Protocol for compiling SCARA DSL into binary wire packets.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.dsl.binary.program import Program
from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICompiler(Protocol):
    '''
        Structural protocol defining contracts for compiling SCARA DSL into binary frames.

        It defines:

            :methods:
                | compile_script - Compiles raw .scara DSL source text into Program.
                | compile_plan - Compiles ITrajectoryPlan into Program.
                | compile_to_bytes - Compiles DSL code directly to raw UART wire byte stream.
    '''

    def compile_script(self, *, source: str) -> Program:
        '''
            Compiles raw .scara source code into a binary program package.

            :param source: Raw .scara DSL script text.
            :return: Compiled Program containing binary frames and byte stream.
        '''

    def compile_plan(self, *, plan: ITrajectoryPlan) -> Program:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: ITrajectoryPlan instance.
            :return: Compiled Program containing binary frames and byte stream.
        '''

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles raw .scara DSL directly into a packed byte stream for UART streaming.

            :param source: Raw .scara DSL script text.
            :return: Raw byte stream with start/end delimiters and CRC-16 checksums.
        '''
