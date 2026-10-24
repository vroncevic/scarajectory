# -*- coding: UTF-8 -*-

'''
Module
    binary_streamer_test.py
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
    Unit tests for BinaryPacketStrategy, BinaryStreamExecutionWorker, and dual-protocol segregated controllers.
'''

from __future__ import annotations

from struct import pack
from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.dsl.binary.axis_peak_steps import AxisPeakSteps
from scaralang.core.model.dsl.binary.binary_program_telemetry import BinaryProgramTelemetry
from scaralang.core.model.dsl.binary.program import BinaryProgram
from scaralang.core.model.dsl.binary.step import BinaryStep, JointStepCoordinates
from scaralang.core.model.protocol.message import MessageId
from scaralang.core.service.compiler.binary.step.discretizer.dependencies import DiscretizerDependencies
from scaralang.core.service.compiler.binary.step.discretizer.factory import StepDiscretizerFactory
from scaralang.core.service.compiler.binary.step.duration.factory import SegmentDurationCalculatorFactory
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.kinematics.transmission.factory import TransmissionFactory
from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.builder.packer import BinaryFramePacker
from scaralang.infrastructure.protocol.builder.system import BinarySystemFrameBuilder
from scaralang.infrastructure.protocol.parser.factory import ParserFactory

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.core.service.streaming.pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.connection.router.factory import RouterFactory
from scarajectory.infrastructure.manipulator.dependencies import ManipulatorDependencies
from scarajectory.infrastructure.manipulator.factory import ManipulatorFactory
from scarajectory.infrastructure.manipulator.provides import ManipulatorProvides
from scarajectory.infrastructure.pacing.provides import PacingProvides
from scarajectory.infrastructure.packet.strategy import BinaryPacketStrategy
from scarajectory.infrastructure.settings.bounds.loader.loader import ScaraBoundsLoader
from scarajectory.infrastructure.settings.dependencies import SettingsDependencies
from scarajectory.infrastructure.settings.factory import SettingsFactory
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.settings.transmission.loader import ScaraTransmissionLoader
from scarajectory.infrastructure.state.dependencies import StateDependencies
from scarajectory.infrastructure.state.factory import StateFactory
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.infrastructure.streaming.assembly.stream_pacing_assembler import StreamPacingAssembler
from scarajectory.infrastructure.streaming.observer.factory import ObserverFactory
from scarajectory.infrastructure.tool.dependencies import ToolDependencies
from scarajectory.infrastructure.tool.factory import ToolFactory
from scarajectory.infrastructure.worker.dependencies import WorkerDependencies
from scarajectory.infrastructure.worker.factory import WorkerFactory
from scarajectory.infrastructure.worker.parser.bundle import ParserBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockByteSender:
    '''Mock byte sender capturing sent byte frames.'''

    def __init__(self, target_list: list[bytes]) -> None:
        self._target_list = target_list

    def send_raw_bytes(self, payload: bytes) -> bool:
        '''Capture raw byte payload.'''
        self._target_list.append(payload)
        return True

    def clear(self) -> None:
        '''Clear recorded payloads.'''
        self._target_list.clear()


class MockStreamer:
    '''Mock streamer capturing string commands and byte payloads.'''

    def __init__(self) -> None:
        self.sent_commands: list[str] = []
        self.sent_bytes: list[bytes] = []
        self.connected: bool = True

    def is_connected(self) -> bool:
        '''Check connection status.'''
        return self.connected

    def send_raw_command(self, cmd: str) -> None:
        '''Capture raw string command.'''
        self.sent_commands.append(cmd)

    def send_raw_bytes(self, payload: bytes) -> bool:
        '''Capture raw byte packet.'''
        self.sent_bytes.append(payload)
        return True


class TestBinaryStreamer(TestCase):
    '''Test cases verifying binary packet formatting, execution worker, and controller commands.'''

    frame_packer: BinaryFramePacker
    system_builder: BinarySystemFrameBuilder
    strategy: BinaryPacketStrategy

    def setUp(self) -> None:
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=bundle)
        )
        settings_provides = SettingsFactory.create(
            SettingsDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        bounds_loader = ScaraBoundsLoader(
            settings_reader=settings_provides.settings_reader,
            bounds_parser=settings_provides.bounds_provides.bounds_parser,
        )
        bounds = bounds_loader.load_bounds()
        transmission_loader = ScaraTransmissionLoader(
            settings_reader=settings_provides.settings_reader,
        )
        transmission = transmission_loader.load_transmission()
        kinematics_provides: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        builder_provides = BuilderFactory.create()
        self.frame_packer = BinaryFramePacker()
        self.system_builder = BinarySystemFrameBuilder(packer=self.frame_packer)
        self.motion_builder = builder_provides.motion
        self.actuator_builder = builder_provides.actuator
        self.frame_parser = ParserFactory.create().parser
        converter = TransmissionFactory.create(
            transmission=transmission
        )
        duration_calc = SegmentDurationCalculatorFactory.create()
        discretizer = StepDiscretizerFactory.create(
            dependencies=DiscretizerDependencies(
                spatial=kinematics_provides.spatial,
                numerical_spatial=kinematics_provides.numerical_spatial,
                transmission=converter,
                duration_calculator=duration_calc,
            )
        )
        self.strategy = BinaryPacketStrategy(
            step_discretizer=discretizer,
            motion_frame_builder=self.motion_builder,
            frame_packer=self.frame_packer,
        )

    def test_binary_packet_strategy(self) -> None:
        '''Tests formatting of waypoints into packed binary move frames.'''
        strategy = self.strategy
        waypoint = TrajectoryWaypoint(x=150.0, y=100.0, z=10.0, speed=50.0, phi=0.0, name='', command='')
        raw_frame = strategy.format_waypoint_packet(waypoint=waypoint, seq_num=1)
        self.assertGreater(len(raw_frame), 0)
        self.assertEqual(raw_frame[0], 0xAA)
        self.assertEqual(raw_frame[1], 0x55)
        self.assertEqual(raw_frame[2], int(MessageId.CMD_MOVE_JOINT_STEPS))
        self.assertEqual(raw_frame[3], 1)
        self.assertEqual(raw_frame[-1], 0x0D)

    def test_manipulator_controller_binary_mode(self) -> None:
        '''Tests robot manipulator commands dispatched as binary frames.'''
        mock = MockStreamer()
        manipulator_provides: ManipulatorProvides = ManipulatorFactory.create(
            ManipulatorDependencies(
                raw_channel=mock,
                system_builder=self.system_builder,
                frame_packer=self.frame_packer,
            )
        )
        motion_ctrl = manipulator_provides.motion_controller
        jog_ctrl = manipulator_provides.jog_controller
        query_ctrl = manipulator_provides.query_controller
        tool_ctrl = ToolFactory.create(
            ToolDependencies(
                raw_channel=mock,
                actuator_builder=self.actuator_builder,
                frame_packer=self.frame_packer,
            )
        ).tool_controller
        self.assertTrue(mock.is_connected())

        self.assertTrue(motion_ctrl.home())
        self.assertTrue(motion_ctrl.enable())
        self.assertTrue(motion_ctrl.disable())
        self.assertTrue(jog_ctrl.set_feedrate_override(120))
        self.assertTrue(tool_ctrl.set_vacuum_pump(True))
        self.assertTrue(tool_ctrl.set_valve(True))
        self.assertTrue(jog_ctrl.jog('X', 5.0))
        self.assertTrue(query_ctrl.query_status())
        self.assertTrue(query_ctrl.query_position())

        self.assertEqual(len(mock.sent_commands), 0)
        self.assertEqual(len(mock.sent_bytes), 9)

        # Verify home frame
        home_frame = mock.sent_bytes[0]
        self.assertEqual(home_frame[0], 0xAA)
        self.assertEqual(home_frame[1], 0x55)
        self.assertEqual(home_frame[2], int(MessageId.CMD_HOME))

        # Verify enable frame
        enable_frame = mock.sent_bytes[1]
        self.assertEqual(enable_frame[2], int(MessageId.CMD_ENABLE))

    def test_binary_stream_execution_worker_lifecycle(self) -> None:
        '''Tests worker lifecycle and processing of binary ACK and move event responses.'''
        pacing_bundle1: PacingProvides = StreamPacingAssembler.assemble(
            queue_capacity=4
        )
        state_controller = StateFactory.create(
            StateDependencies()
        ).stream_state_machine
        observer_dispatcher = ObserverFactory.create().stream_observer_dispatcher
        pacing_config = StreamPacingConfigFactory.create(
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )
        parser_bundle1 = ParserBundle(
            frame_parser=ParserFactory.create().parser,
            response_unpacker=ParserFactory.create().response_unpacker,
        )
        worker_provides1 = WorkerFactory.create(
            WorkerDependencies(
                pacing_bundle=pacing_bundle1,
                packet_strategy=self.strategy,
                byte_sender=MockByteSender([]),
                state_controller=state_controller,
                observer_dispatcher=observer_dispatcher,
                pacing_config=pacing_config,
                parser_bundle=parser_bundle1,
            )
        )
        worker = worker_provides1.execution_worker
        receiver = worker_provides1.bytes_receiver

        session = SessionFactory.create(
            waypoints=[
                TrajectoryWaypoint(x=150.0, y=50.0, z=0.0, speed=10.0, phi=0.0, name='', command=''),
                TrajectoryWaypoint(x=160.0, y=60.0, z=0.0, speed=10.0, phi=0.0, name='', command=''),
            ],
            start_time=0.0,
        )

        worker.start_waypoints(session=session)
        self.assertTrue(worker.is_running())

        # Feed ACK frame
        ack_frame = self.frame_packer.build_frame(
            msg_id=MessageId.RESP_ACK,
            seq_num=0,
            payload=bytes([int(MessageId.CMD_MOVE_JOINT_STEPS), 3]),
        )
        receiver.handle_incoming_bytes(self.frame_packer.pack_frame(frame=ack_frame))

        # Feed MoveEvent DONE for segment 0
        move_done = self.frame_packer.build_frame(
            msg_id=MessageId.RESP_MOVE_EVENT,
            seq_num=1,
            payload=pack('<BI', 2, 0),
        )
        receiver.handle_incoming_bytes(self.frame_packer.pack_frame(frame=move_done))
        self.assertEqual(session.done_count, 1)

        worker.set_paused(True)
        worker.set_paused(False)
        worker.stop()
        self.assertFalse(worker.is_running())

    def test_binary_stream_execution_worker_program(self) -> None:
        '''Tests execution of compiled BinaryProgram instances through execution worker.'''
        pacing_bundle2: PacingProvides = StreamPacingAssembler.assemble(
            queue_capacity=4
        )
        state_controller = StateFactory.create(
            StateDependencies()
        ).stream_state_machine
        observer_dispatcher = ObserverFactory.create().stream_observer_dispatcher
        pacing_config = StreamPacingConfigFactory.create(
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )
        parser_bundle2 = ParserBundle(
            frame_parser=ParserFactory.create().parser,
            response_unpacker=ParserFactory.create().response_unpacker,
        )
        worker = WorkerFactory.create(
            WorkerDependencies(
                pacing_bundle=pacing_bundle2,
                packet_strategy=self.strategy,
                byte_sender=MockByteSender([]),
                state_controller=state_controller,
                observer_dispatcher=observer_dispatcher,
                pacing_config=pacing_config,
                parser_bundle=parser_bundle2,
            )
        ).execution_worker

        step_bytes = self.frame_packer.pack_frame(
            frame=self.system_builder.build_system_cmd(
                msg_id=MessageId.CMD_ENABLE,
                seq_num=0,
            )
        )
        program = BinaryProgram(
            steps=(
                BinaryStep(
                    frame=self.system_builder.build_system_cmd(
                        msg_id=MessageId.CMD_ENABLE,
                        seq_num=0,
                    ),
                    raw_bytes=step_bytes,
                    duration_us=1000,
                    target_steps=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
                    description='ENABLE',
                    line_number=1,
                ),
            ),
            raw_bytes=step_bytes,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=JointStepCoordinates(j1=0, j2=0, z=0, j4=0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=1,
                compiled_steps=1,
                duration_us=1000,
                duration_s=0.001,
                peak_steps=AxisPeakSteps(
                    peak_j1_steps=0,
                    peak_j2_steps=0,
                    peak_z_steps=0,
                    peak_j4_steps=0,
                ),
                total_wire_bytes=len(step_bytes),
            ),
        )
        session = SessionFactory.create_default()

        worker.start_program(session=session, program=program)
        worker.stop()
        self.assertFalse(worker.is_running())

    def test_binary_frame_dispatcher(self) -> None:
        '''Tests binary frame router routing frames to registered handlers.'''
        router = RouterFactory.create().frame_router
        mock_handler = MagicMock()
        router.register_handler(
            int(MessageId.RESP_ACK),
            mock_handler,
        )
        ack_frame = self.frame_packer.build_frame(
            msg_id=int(MessageId.RESP_ACK),
            seq_num=42,
            payload=bytes([1, 15]),
        )
        self.assertTrue(router.route(ack_frame))
        mock_handler.handle_frame.assert_called_once_with(ack_frame)

        # Unknown ID
        dummy_frame = self.frame_packer.build_frame(
            msg_id=int(MessageId.CMD_NONE),
            seq_num=0,
        )
        self.assertFalse(router.route(dummy_frame))


if __name__ == '__main__':
    main()
