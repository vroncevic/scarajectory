# -*- coding: UTF-8 -*-

'''
Module
    binary_compiler_test.py
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
    Unit tests for BinaryCompiler and binary DSL wire framing.
'''

from __future__ import annotations

from pathlib import Path
from sys import path
from struct import pack
from unittest import TestCase, main

pkg_dir = str(Path(__file__).resolve().parent.parent)
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.message_id import MessageId
from scarajectory.core.model.dsl.binary.program import Program
from scarajectory.core.model.dsl.binary.step import Step
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory
from scarajectory.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.dsl.binary.command.command_compiler_factory import CommandCompilerFactory
from scarajectory.core.service.dsl.binary.compiler_factory import CompilerFactory
from scarajectory.core.service.dsl.binary.command.icommand_compiler import ICommandCompiler
from scarajectory.core.service.dsl.binary.icompiler import ICompiler
from scarajectory.core.service.dsl.binary.motion.imotion_compiler import IMotionCompiler
from scarajectory.core.service.dsl.binary.step.istep_discretizer import IStepDiscretizer
from scarajectory.core.service.dsl.binary.motion.motion_compiler_factory import MotionCompilerFactory
from scarajectory.core.service.dsl.binary.step.step_discretizer_factory import StepDiscretizerFactory
from scarajectory.core.service.dsl.compiler.iscara_compiler import IScaraCompiler
from scarajectory.core.service.dsl.compiler.scara_compiler_factory import ScaraCompilerFactory
from scarajectory.core.service.dsl.lexer.iscara_lexer import IScaraLexer
from scarajectory.core.service.dsl.lexer.scara_lexer_factory import ScaraLexerFactory
from scarajectory.core.service.dsl.parser.iscara_parser import IScaraParser
from scarajectory.core.service.dsl.parser.scara_parser_factory import ScaraParserFactory
from scarajectory.core.service.kinematics.ikinematics_service import IKinematicsService
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scarajectory.core.service.communication.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.communication.protocol.ibinary_frame_parser import IBinaryFrameParser

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBinaryCompiler(TestCase):
    '''
        Test cases verifying BinaryCompiler bytecode generation.

        It defines:

            :methods:
                | setUp - Assembles pure DI binary compiler graph via sub-factories.
                | test_compile_script_to_binary_program - Verifies DSL to binary package.
                | test_compile_plan_to_binary - Verifies pre-planned trajectory conversion.
                | test_compile_to_bytes_wire_stream - Verifies wire framing and delimiter bytes.
                | test_roundtrip_frame_parser - Verifies BinaryFrameParser decodes compiler frames.
                | test_custom_sub_compiler_composition - Verifies factory DI with sub-compilers.
                | test_joint_steps_and_robot_status_codecs - Verifies pure models serialization.
                | test_command_compiler_patterns - Verifies match-case dispatching.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures wiring components via sub-factories.
        '''
        config_loader = ScaraConfigLoaderFactory.create()
        self.bounds = config_loader.load_bounds()
        self.transmission = config_loader.load_transmission()
        self.kinematics: IKinematicsService = (
            KinematicsServiceFactory.create(bounds=self.bounds)
        )
        self.validator: ITrajectoryValidator = (
            TrajectoryValidatorFactory.create(
                kinematics=self.kinematics
            )
        )
        self.lexer: IScaraLexer = ScaraLexerFactory.create()
        self.parser: IScaraParser = ScaraParserFactory.create(
            lexer=self.lexer
        )
        self.compiler: IScaraCompiler = ScaraCompilerFactory.create(
            validator=self.validator
        )
        self.discretizer: IStepDiscretizer = StepDiscretizerFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission
        )
        self.frame_builder: IBinaryFrameBuilder = (
            BinaryFrameBuilderFactory.create()
        )
        self.motion_compiler: IMotionCompiler = MotionCompilerFactory.create(
            discretizer=self.discretizer,
            frame_builder=self.frame_builder
        )
        self.command_compiler: ICommandCompiler = CommandCompilerFactory.create(
            frame_builder=self.frame_builder
        )
        self.binary_compiler: ICompiler = (
            CompilerFactory.create(
                lexer=self.lexer,
                parser=self.parser,
                compiler=self.compiler,
                motion_compiler=self.motion_compiler,
                command_compiler=self.command_compiler
            )
        )
        self.frame_parser: IBinaryFrameParser = (
            BinaryFrameParserFactory.create()
        )

    def test_compile_script_to_binary_program(self) -> None:
        '''
            Verifies compiling valid SCARA script into Program package.
        '''
        script = (
            'HOME\n'
            'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
            'PUMP ON\n'
            'WAIT 150\n'
            'MOVE_L X=160.0 Y=60.0 Z=10.0\n'
            'PUMP OFF\n'
        )
        program: Program = self.binary_compiler.compile_script(
            source=script
        )
        self.assertGreater(program.instruction_count, 0)
        self.assertGreater(len(program.steps), 0)
        self.assertGreater(len(program.raw_bytes), 0)

        for step in program.steps:
            self.assertIsInstance(step, Step)
            self.assertEqual(step.raw_bytes[:2], b'\xAA\x55')
            self.assertEqual(step.raw_bytes[-1:], b'\x0D')

    def test_compile_plan_to_binary(self) -> None:
        '''
            Verifies compiling pre-existing TrajectoryPlan into Program.
        '''
        plan = TrajectoryPlanFactory.create()
        plan.add_point(
            Waypoint(x=150.0, y=50.0, z=20.0, phi=0.0, speed=50.0, name='P1', command='')
        )
        plan.add_point(
            Waypoint(x=160.0, y=60.0, z=20.0, phi=0.0, speed=50.0, name='P2', command='')
        )
        plan.add_point(
            Waypoint(x=160.0, y=60.0, z=20.0, phi=0.0, speed=50.0, name='P3', command='<CMD:PUMP#1>')
        )

        program: Program = self.binary_compiler.compile_plan(plan=plan)
        self.assertEqual(program.instruction_count, 3)
        self.assertEqual(len(program.steps), 3)

        tool_step = program.steps[2]
        self.assertIn(b'\x0B', tool_step.raw_bytes)

    def test_compile_to_bytes_wire_stream(self) -> None:
        '''
            Verifies compile_to_bytes emits properly framed wire byte buffer.
        '''
        script = 'MOVE_J X=120.0 Y=80.0 Z=15.0\n'
        stream = self.binary_compiler.compile_to_bytes(source=script)
        self.assertIsInstance(stream, bytes)
        self.assertTrue(stream.startswith(b'\xAA\x55'))
        self.assertTrue(stream.endswith(b'\x0D'))

    def test_roundtrip_frame_parser(self) -> None:
        '''
            Verifies BinaryFrameParser successfully unpacks compiled BinaryFrame.
        '''
        script = 'MOVE_J X=150.0 Y=50.0 Z=20.0\n'
        program = self.binary_compiler.compile_script(source=script)
        first_step = program.steps[0]

        parsed = self.frame_parser.feed_bytes(first_step.raw_bytes)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0].msg_id, first_step.frame.msg_id)
        self.assertEqual(parsed[0].seq_num, first_step.frame.seq_num)
        self.assertEqual(parsed[0].payload, first_step.frame.payload)

    def test_custom_sub_compiler_composition(self) -> None:
        '''
            Verifies wiring BinaryCompiler using explicit sub-factories.
        '''
        from scarajectory.core.service.dsl.binary.motion.motion_compiler_factory import MotionCompilerFactory
        from scarajectory.core.service.dsl.binary.command.command_compiler_factory import CommandCompilerFactory
        motion_comp = MotionCompilerFactory.create(
            discretizer=self.discretizer,
            frame_builder=self.frame_builder
        )
        cmd_comp = CommandCompilerFactory.create(
            frame_builder=self.frame_builder
        )
        custom_compiler = CompilerFactory.create(
            lexer=self.lexer,
            parser=self.parser,
            compiler=self.compiler,
            motion_compiler=motion_comp,
            command_compiler=cmd_comp
        )
        raw = custom_compiler.compile_to_bytes(
            source='HOME\nMOVE_J X=150.0 Y=50.0 Z=20.0\nPUMP ON\n'
        )
        self.assertTrue(raw.startswith(b'\xAA\x55'))
        self.assertTrue(raw.endswith(b'\x0D'))

    def test_joint_steps_and_robot_status_codecs(self) -> None:
        '''
            Verifies pure models JointSteps and RobotStatus serialization via parser.
        '''
        from struct import pack
        from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
        from scarajectory.core.model.communication.telemetry.scara_status import ScaraStatus
        from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser

        steps = JointSteps(
            target_j1_steps=1000,
            target_j2_steps=-500,
            target_z_steps=200,
            target_j4_steps=180,
            duration_us=45000,
            feedrate_scale=100
        )
        frame = self.frame_builder.build_joint_move(seq_num=42, steps=steps)
        unpacked_steps = BinaryFrameParser.unpack_joint_steps(frame.payload)
        self.assertEqual(unpacked_steps.target_j1_steps, 1000)
        self.assertEqual(unpacked_steps.target_j2_steps, -500)
        self.assertEqual(unpacked_steps.target_z_steps, 200)
        self.assertEqual(unpacked_steps.target_j4_steps, 180)
        self.assertEqual(unpacked_steps.duration_us, 45000)

        # 19 bytes status: <BBBiiii
        status_payload = pack('<BBBiiii', 0, 0, 0, 100, 200, 300, 400)
        status = BinaryFrameParser.unpack_scara_status(status_payload)
        self.assertIsInstance(status, ScaraStatus)
        self.assertEqual(status.system_state, 0)
        self.assertFalse(status.is_busy)
        self.assertEqual(status.queue_count, 0)
        self.assertEqual(status.j1_steps, 100)
        self.assertEqual(status.j4_steps, 400)

        # Verify backward-compatible alias unpack_robot_status
        status_alias = BinaryFrameParser.unpack_robot_status(status_payload)
        self.assertIsInstance(status_alias, ScaraStatus)
        self.assertEqual(status_alias.system_state, 0)

    def test_command_compiler_patterns(self) -> None:
        '''
            Verifies CommandCompiler match-case dispatching and StrEnum command handling.
        '''
        from struct import pack
        from scarajectory.core.model.communication.protocol.message_id import MessageId
        from scarajectory.core.service.dsl.binary.command.command_compiler_factory import CommandCompilerFactory

        compiler = CommandCompilerFactory.create(
            frame_builder=self.frame_builder
        )

        # Tool pump commands
        step_pump_on = compiler.compile_command_step(
            command='<CMD:PUMP#1>', seq_num=1, line_num=1
        )
        self.assertEqual(step_pump_on.frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(step_pump_on.frame.payload, b'\x00\x01')

        step_pump_off = compiler.compile_command_step(
            command='PUMP OFF', seq_num=2, line_num=2
        )
        self.assertEqual(step_pump_off.frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(step_pump_off.frame.payload, b'\x00\x00')

        # Tool valve commands
        step_valve_on = compiler.compile_command_step(
            command='VALVE ON', seq_num=3, line_num=3
        )
        self.assertEqual(step_valve_on.frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(step_valve_on.frame.payload, b'\x01\x01')

        step_valve_off = compiler.compile_command_step(
            command='<CMD:VALVE#0>', seq_num=4, line_num=4
        )
        self.assertEqual(step_valve_off.frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(step_valve_off.frame.payload, b'\x01\x00')

        # Wait commands
        step_wait = compiler.compile_command_step(
            command='<CMD:WAIT#250>', seq_num=5, line_num=5
        )
        self.assertEqual(step_wait.frame.msg_id, MessageId.CMD_WAIT)
        self.assertEqual(step_wait.frame.payload, pack('<I', 250))

        step_wait_default = compiler.compile_command_step(
            command='WAIT', seq_num=6, line_num=6
        )
        self.assertEqual(step_wait_default.frame.msg_id, MessageId.CMD_WAIT)
        self.assertEqual(step_wait_default.frame.payload, pack('<I', 100))

        # System commands
        step_home = compiler.compile_command_step(
            command='<CMD:HOME>', seq_num=7, line_num=7
        )
        self.assertEqual(step_home.frame.msg_id, MessageId.CMD_HOME)

        step_enable = compiler.compile_command_step(
            command='ENABLE', seq_num=8, line_num=8
        )
        self.assertEqual(step_enable.frame.msg_id, MessageId.CMD_ENABLE)

        step_disable = compiler.compile_command_step(
            command='<CMD:DISABLE>', seq_num=9, line_num=9
        )
        self.assertEqual(step_disable.frame.msg_id, MessageId.CMD_DISABLE)

        step_hold = compiler.compile_command_step(
            command='<CMD:HOLD>', seq_num=10, line_num=10
        )
        self.assertEqual(step_hold.frame.msg_id, MessageId.CMD_HOLD)

        step_resume = compiler.compile_command_step(
            command='RESUME', seq_num=11, line_num=11
        )
        self.assertEqual(step_resume.frame.msg_id, MessageId.CMD_RESUME)

        step_estop = compiler.compile_command_step(
            command='<CMD:ESTOP>', seq_num=12, line_num=12
        )
        self.assertEqual(step_estop.frame.msg_id, MessageId.CMD_ESTOP)

        # Unknown / ping fallback
        step_ping = compiler.compile_command_step(
            command='UNKNOWN_CMD', seq_num=13, line_num=13
        )
        self.assertEqual(step_ping.frame.msg_id, MessageId.CMD_PING)

    def test_binary_frame_builder_formats_and_tool_cmds(self) -> None:
        '''
            Verifies BinaryFrameBuilder struct format constants and tool commands.
        '''
        self.assertEqual(BinaryFrameBuilder.TOOL_CMD_FORMAT, '<BB')
        self.assertEqual(BinaryFrameBuilder.HEADER_FORMAT, '<BBB')
        self.assertEqual(BinaryFrameBuilder.TRAILER_FORMAT, '<HB')

        # Test tool actuation frame construction (PUMP: tool_id 0)
        pump_on_frame: BinaryFrame = self.frame_builder.build_tool_cmd(
            seq_num=1,
            tool_id=0,
            state=True
        )
        self.assertEqual(pump_on_frame.msg_id, MessageId.CMD_TOOL_PUMP)
        self.assertEqual(pump_on_frame.seq_num, 1)
        self.assertEqual(pump_on_frame.payload, pack('<BB', 0, 1))

        # Test tool actuation frame construction (VALVE: tool_id 1)
        valve_off_frame: BinaryFrame = self.frame_builder.build_tool_cmd(
            seq_num=2,
            tool_id=1,
            state=False
        )
        self.assertEqual(valve_off_frame.msg_id, MessageId.CMD_TOOL_VALVE)
        self.assertEqual(valve_off_frame.seq_num, 2)
        self.assertEqual(valve_off_frame.payload, pack('<BB', 1, 0))

        # Test wire packing
        wire_bytes: bytes = self.frame_builder.pack_frame(frame=pump_on_frame)
        self.assertEqual(wire_bytes[0], BinaryFrameBuilder.SOF1)
        self.assertEqual(wire_bytes[1], BinaryFrameBuilder.SOF2)
        self.assertEqual(wire_bytes[-1], BinaryFrameBuilder.EOF)
        self.assertEqual(len(wire_bytes), 2 + 3 + len(pump_on_frame.payload) + 3)


if __name__ == '__main__':
    main()
