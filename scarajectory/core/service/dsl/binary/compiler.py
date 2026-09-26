# -*- coding: UTF-8 -*-

'''
Module
    compiler.py
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
    Compiles SCARA DSL programs into hardware binary UART packets and frames.
'''

from __future__ import annotations

from scarajectory.core.model.dsl.binary.program import Program
from scarajectory.core.model.dsl.binary.step import Step
from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.dsl.binary.command.icommand_compiler import ICommandCompiler
from scarajectory.core.service.dsl.binary.motion.imotion_compiler import IMotionCompiler
from scarajectory.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.parser.iscara_parser import IScaraParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Compiler:
    '''
        Compiles .scara DSL scripts and TrajectoryPlans into binary UART packets.

        It defines:

            :attributes:
                | _lexer - Dedicated lexical tokenizer protocol.
                | _parser - AST grammar parser orchestrator protocol.
                | _compiler - Macro expander and validator protocol.
                | _motion_compiler - Waypoint to motion frame sub-compiler protocol.
                | _command_compiler - Command to hardware frame sub-compiler protocol.
            :methods:
                | __init__ - Initializes binary compiler with injected component protocols.
                | compile_script - Compiles raw .scara DSL source text into Program.
                | compile_plan - Compiles TrajectoryPlan into Program.
                | compile_to_bytes - Compiles DSL code directly to raw UART wire byte stream.
    '''

    _lexer: IScaraLexer
    _parser: IScaraParser
    _compiler: IScaraCompiler
    _motion_compiler: IMotionCompiler
    _command_compiler: ICommandCompiler

    def __init__(
        self,
        *,
        lexer: IScaraLexer,
        parser: IScaraParser,
        compiler: IScaraCompiler,
        motion_compiler: IMotionCompiler,
        command_compiler: ICommandCompiler
    ) -> None:
        '''
            Initializes binary compiler with injected component protocols.

            :param lexer: Injected IScaraLexer protocol.
            :param parser: Injected IScaraParser protocol.
            :param compiler: Injected IScaraCompiler protocol.
            :param motion_compiler: Injected IMotionCompiler protocol.
            :param command_compiler: Injected ICommandCompiler protocol.
            :exceptions: None.
        '''
        self._lexer = lexer
        self._parser = parser
        self._compiler = compiler
        self._motion_compiler = motion_compiler
        self._command_compiler = command_compiler

    def compile_script(self, *, source: str) -> Program:
        '''
            Compiles raw .scara source code into a binary program package.

            :param source: Raw .scara DSL script text.
            :return: Compiled Program containing binary frames and byte stream.
            :exceptions: ValueError if parsing or validation fails.
        '''
        tokens = self._lexer.tokenize(source=source)
        program = self._parser.parse_tokens(tokens=tokens)
        plan: ITrajectoryPlan = self._compiler.compile(program=program)

        return self.compile_plan(plan=plan)

    def compile_plan(self, *, plan: ITrajectoryPlan) -> Program:
        '''
            Compiles a validated ITrajectoryPlan into a binary program package.

            :param plan: ITrajectoryPlan instance.
            :return: Compiled Program containing binary frames and byte stream.
            :exceptions: ValueError if kinematic solving fails.
        '''
        steps: list[Step] = []
        seq_num: int = 0
        prev_angles: tuple[float, float, float, float] | None = None
        total_duration: int = 0
        peak_steps = [0, 0, 0, 0]

        for idx, pt in enumerate(plan.waypoints):
            seq: int = (seq_num + idx) & 0xFF
            step: Step
            if pt.command:
                step = self._command_compiler.compile_command_step(
                    command=pt.command,
                    seq_num=seq,
                    line_num=idx + 1
                )
            else:
                step, prev_angles = self._motion_compiler.compile_motion_step(
                    waypoint=pt,
                    seq_num=seq,
                    prev_angles=prev_angles,
                    line_num=idx + 1
                )
                for i in range(4):
                    peak_steps[i] = max(peak_steps[i], abs(step.target_steps[i]))

            steps.append(step)
            total_duration += step.duration_us

        raw_bytes: bytes = b''.join(s.raw_bytes for s in steps)

        return Program(
            steps=tuple(steps),
            raw_bytes=raw_bytes,
            total_duration_us=total_duration,
            instruction_count=len(steps),
            step_counts=tuple(peak_steps)
        )

    def compile_to_bytes(self, *, source: str) -> bytes:
        '''
            Compiles raw .scara DSL directly into a packed byte stream for UART streaming.

            :param source: Raw .scara DSL script text.
            :return: Raw byte stream with start/end delimiters and CRC-16 checksums.
            :exceptions: ValueError if compilation fails.
        '''
        program: Program = self.compile_script(source=source)

        return program.raw_bytes
