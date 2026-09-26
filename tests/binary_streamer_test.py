# -*- coding: UTF-8 -*-

"""
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
    Unit tests for BinaryPacketStrategy, BinaryStreamExecutionWorker, and dual-protocol RobotController.
"""

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.message_id import MessageId
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.communication.stream.stream_session import StreamSession
from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.core.model.dsl.binary.program import Program
from scarajectory.core.model.dsl.binary.step import Step
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory
from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory
from scarajectory.core.service.communication.event.binary_frame_dispatcher_factory import BinaryFrameDispatcherFactory
from scarajectory.core.service.communication.stream.session_factory import SessionFactory
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder import BinaryFrameBuilder
from scarajectory.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser import BinaryFrameParser
from scarajectory.infrastructure.communication.protocol.binary.parser.binary_frame_parser_factory import BinaryFrameParserFactory
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy import BinaryPacketStrategy
from scarajectory.infrastructure.communication.streamer.binary_packet_strategy_factory import BinaryPacketStrategyFactory
from scarajectory.infrastructure.communication.streamer.binary_stream_execution_worker import BinaryStreamExecutionWorker
from scarajectory.infrastructure.communication.streamer.binary_stream_execution_worker_factory import BinaryStreamExecutionWorkerFactory
from scarajectory.infrastructure.communication.streamer.flow_controller_factory import FlowControllerFactory
from scarajectory.infrastructure.communication.controller.robot_controller import RobotController
from scarajectory.infrastructure.communication.controller.robot_controller_factory import RobotControllerFactory
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory
from scarajectory.infrastructure.communication.transport.transport_factory import TransportFactory


class MockStreamer:
    def __init__(self) -> None:
        self.sent_commands: list[str] = []
        self.sent_bytes: list[bytes] = []
        self.connected: bool = True

    def is_connected(self) -> bool:
        return self.connected

    def send_raw_command(self, cmd: str) -> None:
        self.sent_commands.append(cmd)

    def send_raw_bytes(self, data: bytes) -> bool:
        self.sent_bytes.append(data)
        return True


class TestBinaryStreamer(TestCase):
    def setUp(self) -> None:
        loader = ScaraConfigLoaderFactory.create()
        self.bounds = loader.load_bounds()
        self.transmission = loader.load_transmission()
        self.kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        self.frame_builder = BinaryFrameBuilderFactory.create()
        self.frame_parser = BinaryFrameParserFactory.create()

    def test_binary_packet_strategy(self) -> None:
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        wp = WaypointFactory.create(x=150.0, y=100.0, z=10.0, speed=50.0)
        raw_frame = strategy.format_waypoint_packet(waypoint=wp, seq_num=1)
        self.assertGreater(len(raw_frame), 0)
        self.assertEqual(raw_frame[0], 0xAA)
        self.assertEqual(raw_frame[1], 0x55)
        self.assertEqual(raw_frame[2], int(MessageId.CMD_MOVE_JOINT_STEPS))
        self.assertEqual(raw_frame[3], 1)
        self.assertEqual(raw_frame[-1], 0x0D)

    def test_robot_controller_binary_mode(self) -> None:
        mock = MockStreamer()
        ctrl = RobotControllerFactory.create(
            mock,
            protocol_mode=ProtocolMode.BINARY,
        )
        self.assertTrue(ctrl.is_connected())

        self.assertTrue(ctrl.home())
        self.assertTrue(ctrl.enable())
        self.assertTrue(ctrl.disable())
        self.assertTrue(ctrl.set_feedrate_override(120))
        self.assertTrue(ctrl.set_vacuum_pump(True))
        self.assertTrue(ctrl.set_valve(True))
        self.assertTrue(ctrl.jog('X', 5.0))
        self.assertTrue(ctrl.query_status())
        self.assertTrue(ctrl.query_position())

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

    def test_robot_controller_ascii_mode(self) -> None:
        mock = MockStreamer()
        ctrl = RobotControllerFactory.create(
            mock,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertTrue(ctrl.is_connected())

        self.assertTrue(ctrl.home())
        self.assertTrue(ctrl.enable())
        self.assertTrue(ctrl.disable())

        self.assertEqual(len(mock.sent_bytes), 0)
        self.assertEqual(len(mock.sent_commands), 3)
        self.assertIn('HOME', mock.sent_commands[0])
        self.assertIn('ENABLE', mock.sent_commands[1])
        self.assertIn('DISABLE', mock.sent_commands[2])

    def test_binary_stream_execution_worker_lifecycle(self) -> None:
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        flow = FlowControllerFactory.create(capacity=4)
        sent_chunks: list[bytes] = []
        progress_calls: list[str] = []
        state_changes: list[StreamState] = []

        worker = BinaryStreamExecutionWorkerFactory.create(
            flow_controller=flow,
            packet_strategy=strategy,
            send_bytes=lambda b: sent_chunks.append(b) is None,
            notify_progress=lambda e: progress_calls.append(e),
            notify_log=lambda m, o: None,
            on_state_change=lambda s: state_changes.append(s),
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )

        waypoints = [
            WaypointFactory.create(x=150.0, y=50.0, z=0.0, speed=10.0),
            WaypointFactory.create(x=160.0, y=60.0, z=0.0, speed=10.0),
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
        from struct import pack
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
        strategy = BinaryPacketStrategyFactory.create(
            kinematics=self.kinematics,
            transmission=self.transmission,
        )
        flow = FlowControllerFactory.create(capacity=4)
        sent_chunks: list[bytes] = []

        worker = BinaryStreamExecutionWorkerFactory.create(
            flow_controller=flow,
            packet_strategy=strategy,
            send_bytes=lambda b: sent_chunks.append(b) is None,
            notify_progress=lambda e: None,
            notify_log=lambda m, o: None,
            on_state_change=lambda s: None,
            send_delay=0.001,
            throttle_delay=0.001,
            poll_delay=0.001,
        )

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
        program = Program(
            steps=(step,),
            raw_bytes=step_bytes,
            total_duration_us=1000,
            instruction_count=1,
            step_counts=(0, 0, 0, 0),
        )
        session = SessionFactory.create(waypoints=())

        worker.start_program(session=session, program=program)
        worker.stop()
        self.assertFalse(worker.is_running())

    def test_binary_frame_dispatcher(self) -> None:
        dispatcher = BinaryFrameDispatcherFactory.create()
        dispatched_acks: list[int] = []
        dispatcher.register_handler(
            MessageId.RESP_ACK,
            lambda f: dispatched_acks.append(f.seq_num),
        )
        ack_frame = self.frame_builder.build_frame(
            msg_id=MessageId.RESP_ACK,
            seq_num=42,
            payload=bytes([1, 15]),
        )
        self.assertTrue(dispatcher.dispatch(ack_frame))
        self.assertEqual(dispatched_acks, [42])

        # Unknown ID
        dummy_frame = self.frame_builder.build_frame(
            msg_id=MessageId.CMD_NONE,
            seq_num=0,
        )
        self.assertFalse(dispatcher.dispatch(dummy_frame))


if __name__ == '__main__':
    main()
