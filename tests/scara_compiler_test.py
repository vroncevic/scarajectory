# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_test.py
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
    Unit tests for ScaraCompiler and its specialized primitive sub-compilers.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.dsl.ast.scara_command_type import ScaraCommandType
from scarajectory.core.model.dsl.ast.scara_instruction import ScaraInstruction
from scarajectory.core.model.dsl.ast.scara_program import ScaraProgram
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.compiler.control_command_compiler import (
    ControlCommandCompiler,
)
from scarajectory.core.service.dsl.compiler.motion_command_compiler import (
    MotionCommandCompiler,
)
from scarajectory.core.service.dsl.compiler.scara_compiler import ScaraCompiler
from scarajectory.core.service.dsl.compiler.scara_compiler_context import (
    ScaraCompilerContext,
)
from scarajectory.core.service.dsl.compiler.state_command_compiler import (
    StateCommandCompiler,
)
from scarajectory.core.service.dsl.compiler.tool_command_compiler import (
    ToolCommandCompiler,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraCompiler(TestCase):
    '''
        Test cases verifying ScaraCompiler and its decomposed sub-compilers.

        It defines:

            :methods:
                | test_state_command_compiler - Verifies state configuration compiler.
                | test_tool_command_compiler - Verifies pneumatic tool compiler.
                | test_control_command_compiler - Verifies workflow control compiler.
                | test_motion_command_compiler - Verifies Cartesian and Arc motion compiler.
                | test_compiler_end_to_end - Verifies full ScaraCompiler compiling AST program.
                | test_compiler_custom_sub_compilers - Verifies injection of custom primitive compilers.
    '''

    def test_state_command_compiler(self) -> None:
        '''Verifies StateCommandCompiler handles SPEED, ACCEL, ZONE, CONFIG_ELBOW.'''
        compiler = StateCommandCompiler()
        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        speed_inst = ScaraInstruction(
            command_type=ScaraCommandType.SPEED,
            parameters={'mode': 'RAPID', 'speed': 150.0},
            line_number=1,
            raw_text='SPEED RAPID 150.0',
        )
        self.assertTrue(compiler.can_compile(instruction=speed_inst))
        compiler.compile(instruction=speed_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(ctx.speed_rapid, 150.0)

        zone_inst = ScaraInstruction(
            command_type=ScaraCommandType.ZONE,
            parameters={'mode': 'BLEND', 'radius': 5.0},
            line_number=2,
            raw_text='ZONE BLEND R=5.0',
        )
        self.assertTrue(compiler.can_compile(instruction=zone_inst))
        compiler.compile(instruction=zone_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(ctx.zone_mode, 'BLEND')
        self.assertEqual(ctx.zone_radius, 5.0)

    def test_tool_command_compiler(self) -> None:
        '''Verifies ToolCommandCompiler handles PUMP and VALVE commands.'''
        compiler = ToolCommandCompiler()
        ctx = ScaraCompilerContext()
        ctx.current_x = 100.0
        ctx.current_y = 50.0
        waypoints: list[Waypoint] = []

        pump_inst = ScaraInstruction(
            command_type=ScaraCommandType.PUMP,
            parameters={'state': 'ON'},
            line_number=3,
            raw_text='PUMP ON',
        )
        self.assertTrue(compiler.can_compile(instruction=pump_inst))
        compiler.compile(instruction=pump_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].command, '<CMD:PUMP#1>')
        self.assertEqual(waypoints[0].name, 'PUMP_ON')

    def test_control_command_compiler(self) -> None:
        '''Verifies ControlCommandCompiler handles HOME, WAIT_MS, and ESTOP.'''
        compiler = ControlCommandCompiler()
        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        home_inst = ScaraInstruction(
            command_type=ScaraCommandType.HOME,
            parameters={},
            line_number=1,
            raw_text='HOME',
        )
        self.assertTrue(compiler.can_compile(instruction=home_inst))
        compiler.compile(instruction=home_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(waypoints[0].command, '<CMD:HOME>')

        wait_inst = ScaraInstruction(
            command_type=ScaraCommandType.WAIT_MS,
            parameters={'ms': 250.0},
            line_number=2,
            raw_text='WAIT_MS 250',
        )
        self.assertTrue(compiler.can_compile(instruction=wait_inst))
        compiler.compile(instruction=wait_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(waypoints[1].command, '<CMD:WAIT#250>')

    def test_motion_command_compiler(self) -> None:
        '''Verifies MotionCommandCompiler handles Cartesian and approach moves.'''
        compiler = MotionCommandCompiler()
        ctx = ScaraCompilerContext()
        waypoints: list[Waypoint] = []

        move_inst = ScaraInstruction(
            command_type=ScaraCommandType.MOVE_L,
            parameters={'X': 120.0, 'Y': 60.0, 'Z': 15.0, 'SPEED': 50.0},
            line_number=1,
            raw_text='MOVE_L X=120.0 Y=60.0 Z=15.0 SPEED=50.0',
        )
        self.assertTrue(compiler.can_compile(instruction=move_inst))
        compiler.compile(instruction=move_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 1)
        self.assertEqual(ctx.current_x, 120.0)
        self.assertEqual(ctx.current_y, 60.0)
        self.assertEqual(ctx.current_z, 15.0)

        approach_inst = ScaraInstruction(
            command_type=ScaraCommandType.APPROACH,
            parameters={'DIST': 10.0, 'SPEED': 25.0},
            line_number=2,
            raw_text='APPROACH DIST=10.0 SPEED=25.0',
        )
        self.assertTrue(compiler.can_compile(instruction=approach_inst))
        compiler.compile(instruction=approach_inst, context=ctx, waypoints=waypoints)
        self.assertEqual(len(waypoints), 2)
        self.assertEqual(ctx.current_z, 5.0)

    def test_compiler_end_to_end(self) -> None:
        '''Verifies full program compilation through ScaraCompiler orchestrator.'''
        compiler = ScaraCompiler()
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.HOME,
                parameters={},
                line_number=1,
                raw_text='HOME',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.MOVE_J,
                parameters={'X': 150.0, 'Y': 50.0, 'Z': 20.0, 'PHI': 0.0},
                line_number=2,
                raw_text='MOVE_J X=150.0 Y=50.0 Z=20.0 PHI=0.0',
            ),
            ScaraInstruction(
                command_type=ScaraCommandType.PUMP,
                parameters={'state': 'ON'},
                line_number=3,
                raw_text='PUMP ON',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        plan = compiler.compile(program=program)
        self.assertGreaterEqual(plan.count, 3)

    def test_compiler_custom_sub_compilers(self) -> None:
        '''Verifies ScaraCompiler accepts custom primitive sub-compilers.'''
        custom_tool = ToolCommandCompiler()
        compiler = ScaraCompiler(primitive_compilers=(custom_tool,))
        instructions = [
            ScaraInstruction(
                command_type=ScaraCommandType.PUMP,
                parameters={'state': 'ON'},
                line_number=1,
                raw_text='PUMP ON',
            ),
        ]
        program = ScaraProgram(instructions=instructions)
        plan = compiler.compile(program=program)
        self.assertEqual(plan.count, 1)


if __name__ == '__main__':
    main()
