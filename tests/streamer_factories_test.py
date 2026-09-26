# -*- coding: UTF-8 -*-

'''
Module
    streamer_factories_test.py
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
    Unit test suite validating communication and streaming factory modules.
'''

from __future__ import annotations

from sys import path
from os.path import abspath, dirname
from unittest import TestCase

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.service.communication.protocol.icommand_formatter import ICommandFormatter
from scarajectory.core.service.communication.protocol.iprotocol_parser import IProtocolParser
from scarajectory.core.service.communication.controller.irobot_controller import IRobotController
from scarajectory.core.service.communication.stream.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.model.communication.stream.stream_state import StreamState
from scarajectory.infrastructure.communication.protocol.ascii.formatter.command_formatter_factory import CommandFormatterFactory
from scarajectory.infrastructure.communication.protocol.ascii.parser.protocol_parser_factory import ProtocolParserFactory
from scarajectory.infrastructure.communication.streamer.flow_controller_factory import FlowControllerFactory
from scarajectory.infrastructure.communication.controller.robot_controller_factory import RobotControllerFactory
from scarajectory.infrastructure.communication.streamer.stream_execution_worker_factory import StreamExecutionWorkerFactory
from scarajectory.infrastructure.communication.streamer.stream_observer_dispatcher_factory import StreamObserverDispatcherFactory
from scarajectory.infrastructure.communication.streamer.stream_state_machine_factory import StreamStateMachineFactory
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestStreamerFactories(TestCase):
    '''
        Test cases validating creation and protocol conformance for streamer factories.
    '''

    def test_protocol_parser_factory(self) -> None:
        '''
            Tests ProtocolParser creation and IProtocolParser structural conformance.
        '''
        parser = ProtocolParserFactory.create()
        self.assertIsInstance(parser, IProtocolParser)
        self.assertTrue(parser.is_action_done('<RESP:ACK#PUMP_ON>'))
        self.assertTrue(parser.is_homing_failed('HOMING_FAILED'))
        self.assertFalse(parser.is_buffer_full('OK'))

    def test_command_formatter_factory(self) -> None:
        '''
            Tests CommandFormatter creation and ICommandFormatter structural conformance.
        '''
        formatter = CommandFormatterFactory.create()
        self.assertIsInstance(formatter, ICommandFormatter)

    def test_flow_controller_factory(self) -> None:
        '''
            Tests FlowController creation with custom and default capacity.
        '''
        fc1 = FlowControllerFactory.create()
        self.assertEqual(fc1.capacity, 16)
        self.assertTrue(fc1.is_barrier_clear())

        fc2 = FlowControllerFactory.create(capacity=32)
        self.assertEqual(fc2.capacity, 32)

    def test_stream_state_machine_factory(self) -> None:
        '''
            Tests StreamStateMachine creation and initial states.
        '''
        sm = StreamStateMachineFactory.create()
        self.assertEqual(sm.state, StreamState.IDLE)
        self.assertFalse(sm.is_active())

        sm_paused = StreamStateMachineFactory.create(initial_state=StreamState.PAUSED)
        self.assertEqual(sm_paused.state, StreamState.PAUSED)
        self.assertTrue(sm_paused.is_active())

    def test_stream_observer_dispatcher_factory(self) -> None:
        '''
            Tests StreamObserverDispatcher creation.
        '''
        dispatcher = StreamObserverDispatcherFactory.create()
        self.assertFalse(dispatcher.has_observer())

    def test_stream_execution_worker_factory(self) -> None:
        '''
            Tests StreamExecutionWorker creation via factory.
        '''
        fc = FlowControllerFactory.create()
        worker = StreamExecutionWorkerFactory.create(
            flow_controller=fc,
            send_command=lambda cmd: True,
            notify_progress=lambda err: None,
            notify_log=lambda msg, out: None,
            on_state_change=lambda state: None,
        )
        self.assertFalse(worker.is_running())

    def test_trajectory_streamer_and_robot_controller_factories(self) -> None:
        '''
            Tests TrajectoryStreamerFactory and RobotControllerFactory assembly.
        '''
        streamer = TrajectoryStreamerFactory.create_default()
        self.assertIsInstance(streamer, ITrajectoryStreamer)

        robot_ctrl = RobotControllerFactory.create(streamer)
        self.assertIsInstance(robot_ctrl, IRobotController)
        self.assertIsInstance(streamer.get_robot_controller(), IRobotController)
