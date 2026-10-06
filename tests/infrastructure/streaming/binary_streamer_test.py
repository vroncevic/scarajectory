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
from scaralang.core.model.dsl.binary.step import Step
from scaralang.core.model.protocol.message_id import MessageId
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scaralang.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.streaming.session_factory import SessionFactory
from scarajectory.core.service.streaming.stream_pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.barrier.flow_barrier_factory import FlowBarrierFactory
from scarajectory.infrastructure.event.binary_frame_dispatcher_factory import BinaryFrameDispatcherFactory
from scarajectory.infrastructure.manipulator.jog_controller_factory import JogControllerFactory
from scarajectory.infrastructure.manipulator.motion_controller_factory import MotionControllerFactory
from scarajectory.infrastructure.manipulator.query_controller_factory import QueryControllerFactory
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle
from scarajectory.infrastructure.pacing.flow_pacing_bundle_factory import FlowPacingBundleFactory
from scarajectory.infrastructure.packet.binary_packet_strategy_factory import BinaryPacketStrategyFactory
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.infrastructure.settings.transmission.scara_transmission_loader_factory import ScaraTransmissionLoaderFactory
from scarajectory.infrastructure.state.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.streaming.observer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.tool.tool_controller_factory import ToolControllerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_execution_worker_factory import BinaryStreamExecutionWorkerFactory
from scarajectory.infrastructure.worker.binary.binary_stream_runner_bundle import BinaryStreamRunnerBundle

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

    def setUp(self) -> None:
        self.bounds = ScaraBoundsLoaderFactory.create().load_bounds()
        self.transmission = ScaraTransmissionLoaderFactory.create().load_transmission()
        self.kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        self.frame_builder = BinaryFrameBuilderFactory.create()
        self.frame_parser = BinaryFrameParserFactory.create()

    def test_binary_packet_strategy(self) -> None:
        '''Tests formatting of waypoints into packed binary move frames.'''
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        waypoint = Waypoint(x=150.0, y=100.0, z=10.0, speed=50.0)
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
        motion_ctrl = MotionControllerFactory.create(
            raw_channel=mock,
            frame_builder=self.frame_builder,
            protocol_mode=ProtocolMode.BINARY,
        )
        tool_ctrl = ToolControllerFactory.create(
            raw_channel=mock,
            frame_builder=self.frame_builder,
            protocol_mode=ProtocolMode.BINARY,
        )
        jog_ctrl = JogControllerFactory.create(
            raw_channel=mock,
            frame_builder=self.frame_builder,
            protocol_mode=ProtocolMode.BINARY,
        )
        query_ctrl = QueryControllerFactory.create(
            raw_channel=mock,
            frame_builder=self.frame_builder,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.assertTrue(motion_ctrl.is_connected())

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

    def test_manipulator_controller_ascii_mode(self) -> None:
        '''Tests robot manipulator commands dispatched as ASCII strings.'''
        mock = MockStreamer()
        motion_ctrl = MotionControllerFactory.create(
            raw_channel=mock,
            frame_builder=self.frame_builder,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertTrue(motion_ctrl.is_connected())

        self.assertTrue(motion_ctrl.home())
        self.assertTrue(motion_ctrl.enable())
        self.assertTrue(motion_ctrl.disable())

        self.assertEqual(len(mock.sent_bytes), 0)
        self.assertEqual(len(mock.sent_commands), 3)
        self.assertIn('HOME', mock.sent_commands[0])
        self.assertIn('ENABLE', mock.sent_commands[1])
        self.assertIn('DISABLE', mock.sent_commands[2])

    def test_binary_stream_execution_worker_lifecycle(self) -> None:
        '''Tests worker lifecycle and processing of binary ACK and move event responses.'''
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        barrier1 = FlowBarrierFactory.create()
        pacing_bundle1: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier1, capacity=4
        )
        sent_chunks: list[bytes] = []
        byte_sender = MockByteSender(sent_chunks)
        state_controller = StreamStateMachineFactory.create()
        observer_dispatcher = StreamObserverDispatcherFactory.create()
        pacing_config = StreamPacingConfigFactory.create(
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )

        runner_bundle1 = BinaryStreamRunnerBundle(
            pacing_bundle=pacing_bundle1,
            packet_strategy=strategy,
            byte_sender=byte_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )
        worker = BinaryStreamExecutionWorkerFactory.create(runner_bundle1)

        waypoints = [
            Waypoint(x=150.0, y=50.0, z=0.0, speed=10.0),
            Waypoint(x=160.0, y=60.0, z=0.0, speed=10.0),
        ]
        session = SessionFactory.create(waypoints=waypoints)

        worker.start(session=session)
        self.assertTrue(worker.is_running())

        # Feed ACK frame
        ack_frame = self.frame_builder.build_frame(
            msg_id=MessageId.RESP_ACK,
            seq_num=0,
            payload=bytes([int(MessageId.CMD_MOVE_JOINT_STEPS), 3]),
        )
        worker.handle_incoming_bytes(self.frame_builder.pack_frame(frame=ack_frame))

        # Feed MoveEvent DONE for segment 0
        move_done = self.frame_builder.build_frame(
            msg_id=MessageId.RESP_MOVE_EVENT,
            seq_num=1,
            payload=pack('<BI', 2, 0),
        )
        worker.handle_incoming_bytes(self.frame_builder.pack_frame(frame=move_done))
        self.assertEqual(session.done_count, 1)

        worker.pause()
        worker.resume()
        worker.stop()
        self.assertFalse(worker.is_running())

    def test_binary_stream_execution_worker_program(self) -> None:
        '''Tests execution of compiled BinaryProgram instances through execution worker.'''
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        barrier2 = FlowBarrierFactory.create()
        pacing_bundle2: FlowPacingBundle = FlowPacingBundleFactory.create(
            barrier=barrier2, capacity=4
        )
        sent_chunks: list[bytes] = []
        byte_sender = MockByteSender(sent_chunks)
        state_controller = StreamStateMachineFactory.create()
        observer_dispatcher = StreamObserverDispatcherFactory.create()
        pacing_config = StreamPacingConfigFactory.create(
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )

        runner_bundle2 = BinaryStreamRunnerBundle(
            pacing_bundle=pacing_bundle2,
            packet_strategy=strategy,
            byte_sender=byte_sender,
            state_controller=state_controller,
            observer_dispatcher=observer_dispatcher,
            pacing_config=pacing_config,
        )
        worker = BinaryStreamExecutionWorkerFactory.create(runner_bundle2)

        step_frame = self.frame_builder.build_system_cmd(
            msg_id=MessageId.CMD_ENABLE,
            seq_num=0,
        )
        step_bytes = self.frame_builder.pack_frame(frame=step_frame)
        step = Step(
            frame=step_frame,
            raw_bytes=step_bytes,
            duration_us=1000,
            target_steps=(0, 0, 0, 0),
            description='ENABLE',
            line_number=1,
        )
        program = BinaryProgram(
            steps=(step,),
            raw_bytes=step_bytes,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(0, 0, 0, 0),
            telemetry=BinaryProgramTelemetry(
                source_instructions=1,
                compiled_steps=1,
                duration_us=1000,
                duration_s=0.001,
                peak_steps=AxisPeakSteps(),
                total_wire_bytes=len(step_bytes),
            ),
        )
        session = SessionFactory.create(waypoints=())

        worker.start_program(session=session, program=program)
        worker.stop()
        self.assertFalse(worker.is_running())

    def test_binary_frame_dispatcher(self) -> None:
        '''Tests binary frame dispatcher dispatching frames to registered handlers.'''
        dispatcher = BinaryFrameDispatcherFactory.create()
        mock_handler = MagicMock()
        dispatcher.register_handler(
            int(MessageId.RESP_ACK),
            mock_handler,
        )
        ack_frame = self.frame_builder.build_frame(
            msg_id=int(MessageId.RESP_ACK),
            seq_num=42,
            payload=bytes([1, 15]),
        )
        self.assertTrue(dispatcher.dispatch(ack_frame))
        mock_handler.handle_frame.assert_called_once_with(ack_frame)

        # Unknown ID
        dummy_frame = self.frame_builder.build_frame(
            msg_id=int(MessageId.CMD_NONE),
            seq_num=0,
        )
        self.assertFalse(dispatcher.dispatch(dummy_frame))


if __name__ == '__main__':
    main()
