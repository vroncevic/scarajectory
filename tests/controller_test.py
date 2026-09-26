# -*- coding: UTF-8 -*-

'''
Module
    controller_test.py
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
    Unit tests for segregated controller adapters, factories, and composite RobotController facade.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.communication.controller.ijog_controller import IJogController
from scarajectory.core.service.communication.controller.imotion_controller import IMotionController
from scarajectory.core.service.communication.controller.iquery_controller import IQueryController
from scarajectory.core.service.communication.controller.irobot_controller import IRobotController
from scarajectory.core.service.communication.controller.itool_controller import IToolController
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.infrastructure.communication.controller.jog_controller_factory import JogControllerFactory
from scarajectory.infrastructure.communication.controller.motion_controller_factory import MotionControllerFactory
from scarajectory.infrastructure.communication.controller.query_controller_factory import QueryControllerFactory
from scarajectory.infrastructure.communication.controller.robot_controller_factory import RobotControllerFactory
from scarajectory.infrastructure.communication.controller.tool_controller_factory import ToolControllerFactory
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory
from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ControllerTest(TestCase):
    '''
    Unit tests verifying ISP compliance of segregated controllers and RobotController facade.

    It defines:

        :methods:
            | setUp - Prepares transport, streamer, and frame builder test fixtures.
            | test_motion_controller_contract - Tests MotionController satisfies IMotionController.
            | test_jog_controller_contract - Tests JogController satisfies IJogController.
            | test_tool_controller_contract - Tests ToolController satisfies IToolController.
            | test_query_controller_contract - Tests QueryController satisfies IQueryController.
            | test_robot_controller_composite - Tests RobotController satisfies IRobotController.
            | test_robot_controller_accessors - Tests access to internal sub-controllers.
    '''

    def setUp(self) -> None:
        '''
        Sets up shared fixtures for controller testing.
        '''
        self._transport = SerialTransport()
        self._streamer = TrajectoryStreamerFactory.create(transport=self._transport)
        self._frame_builder: IBinaryFrameBuilder = BinaryFrameBuilderFactory.create()

    def test_motion_controller_contract(self) -> None:
        '''
        Tests MotionController satisfies IMotionController structural protocol.
        '''
        motion_ctrl = MotionControllerFactory.create(
            raw_channel=self._streamer,
            frame_builder=self._frame_builder,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(motion_ctrl, IMotionController)
        self.assertFalse(motion_ctrl.home())
        self.assertFalse(motion_ctrl.enable())
        self.assertFalse(motion_ctrl.disable())
        self.assertTrue(motion_ctrl.clear_fault())

        motion_ctrl.set_protocol_mode(ProtocolMode.BINARY)
        self.assertFalse(motion_ctrl.home())
        self.assertFalse(motion_ctrl.enable())
        self.assertFalse(motion_ctrl.disable())
        self.assertFalse(motion_ctrl.clear_fault())

    def test_jog_controller_contract(self) -> None:
        '''
        Tests JogController satisfies IJogController structural protocol.
        '''
        jog_ctrl = JogControllerFactory.create(
            raw_channel=self._streamer,
            frame_builder=self._frame_builder,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(jog_ctrl, IJogController)
        self.assertFalse(jog_ctrl.jog('X', 5.0))
        self.assertFalse(jog_ctrl.set_feedrate_override(120))

        jog_ctrl.set_protocol_mode(ProtocolMode.BINARY)
        self.assertFalse(jog_ctrl.jog('X', 5.0))
        self.assertFalse(jog_ctrl.set_feedrate_override(120))

    def test_tool_controller_contract(self) -> None:
        '''
        Tests ToolController satisfies IToolController structural protocol.
        '''
        tool_ctrl = ToolControllerFactory.create(
            raw_channel=self._streamer,
            frame_builder=self._frame_builder,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(tool_ctrl, IToolController)
        self.assertFalse(tool_ctrl.set_vacuum_pump(True))
        self.assertFalse(tool_ctrl.set_valve(True))
        self.assertFalse(tool_ctrl.pulse_purge_valve())

        tool_ctrl.set_protocol_mode(ProtocolMode.BINARY)
        self.assertFalse(tool_ctrl.set_vacuum_pump(True))
        self.assertFalse(tool_ctrl.set_valve(True))
        self.assertFalse(tool_ctrl.pulse_purge_valve())

    def test_query_controller_contract(self) -> None:
        '''
        Tests QueryController satisfies IQueryController structural protocol.
        '''
        query_ctrl = QueryControllerFactory.create(
            raw_channel=self._streamer,
            frame_builder=self._frame_builder,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(query_ctrl, IQueryController)
        self.assertFalse(query_ctrl.query_status())
        self.assertFalse(query_ctrl.query_position())

        query_ctrl.set_protocol_mode(ProtocolMode.BINARY)
        self.assertFalse(query_ctrl.query_status())
        self.assertFalse(query_ctrl.query_position())

    def test_robot_controller_composite(self) -> None:
        '''
        Tests RobotController satisfies IRobotController, IMotionController, IJogController, IToolController, IQueryController.
        '''
        robot_ctrl = RobotControllerFactory.create(
            raw_channel=self._streamer,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(robot_ctrl, IRobotController)
        self.assertIsInstance(robot_ctrl, IMotionController)
        self.assertIsInstance(robot_ctrl, IJogController)
        self.assertIsInstance(robot_ctrl, IToolController)
        self.assertIsInstance(robot_ctrl, IQueryController)

        self.assertFalse(robot_ctrl.is_connected())
        self.assertFalse(robot_ctrl.home())
        self.assertFalse(robot_ctrl.jog('Y', -2.0))
        self.assertFalse(robot_ctrl.set_vacuum_pump(False))
        self.assertFalse(robot_ctrl.query_status())

    def test_robot_controller_accessors(self) -> None:
        '''
        Tests that RobotController exposes direct accessors for granular controllers.
        '''
        robot_ctrl = RobotControllerFactory.create(
            raw_channel=self._streamer,
            protocol_mode=ProtocolMode.ASCII,
        )
        self.assertIsInstance(robot_ctrl.get_motion_controller(), IMotionController)
        self.assertIsInstance(robot_ctrl.get_jog_controller(), IJogController)
        self.assertIsInstance(robot_ctrl.get_tool_controller(), IToolController)
        self.assertIsInstance(robot_ctrl.get_query_controller(), IQueryController)


if __name__ == '__main__':
    main()
