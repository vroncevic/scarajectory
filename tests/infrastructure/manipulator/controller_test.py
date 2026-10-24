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
    Unit tests verifying ISP compliance of segregated controllers.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaracom.transport.factory import TransportFactory

from scaralang.infrastructure.protocol.builder.factory import BuilderFactory
from scaralang.infrastructure.protocol.builder.provides import BuilderProvides

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.core.service.tool.iactuator import IPurgeValveActuator
from scarajectory.core.service.tool.icontroller import IToolController
from scarajectory.infrastructure.manipulator.jog.dependencies import JogDependencies
from scarajectory.infrastructure.manipulator.jog.factory import JogControllerFactory
from scarajectory.infrastructure.manipulator.motion.dependencies import MotionDependencies
from scarajectory.infrastructure.manipulator.motion.factory import MotionControllerFactory
from scarajectory.infrastructure.manipulator.query.dependencies import QueryDependencies
from scarajectory.infrastructure.manipulator.query.factory import QueryControllerFactory
from scarajectory.infrastructure.streaming.assembly.stream_pipeline_assembler import StreamPipelineAssembler
from scarajectory.infrastructure.streaming.provides import StreamingProvides
from scarajectory.infrastructure.tool.dependencies import ToolDependencies
from scarajectory.infrastructure.tool.factory import ToolFactory

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
    Unit tests verifying ISP compliance of segregated controllers.

    It defines:

        :methods:
            | setUp - Prepares transport, streaming bundle, and frame builder fixtures.
            | test_motion_controller_contract - Tests MotionController satisfies IMotionController.
            | test_jog_controller_contract - Tests JogController satisfies IJogController.
            | test_tool_controller_contract - Tests ToolController satisfies IToolController.
            | test_query_controller_contract - Tests QueryController satisfies IQueryController.
    '''

    def setUp(self) -> None:
        '''
        Sets up shared fixtures for controller testing.
        '''
        self._transport = TransportFactory.create()
        self._streaming: StreamingProvides = StreamPipelineAssembler.assemble(
            transport=self._transport
        )
        self._builders: BuilderProvides = BuilderFactory.create()

    def test_motion_controller_contract(self) -> None:
        '''
            Tests MotionController satisfies IMotionController structural protocol.

            :exceptions: None.
        '''
        motion_ctrl = MotionControllerFactory.create(
            MotionDependencies(
                raw_channel=self._streaming.raw_channel,
                system_builder=self._builders.system,
                frame_packer=self._builders.packer,
            )
        ).motion_controller
        self.assertIsInstance(motion_ctrl, IMotionController)
        self.assertFalse(motion_ctrl.home())
        self.assertFalse(motion_ctrl.enable())
        self.assertFalse(motion_ctrl.disable())
        self.assertFalse(motion_ctrl.clear_fault())

    def test_jog_controller_contract(self) -> None:
        '''
            Tests JogController satisfies IJogController structural protocol.

            :exceptions: None.
        '''
        jog_ctrl = JogControllerFactory.create(
            JogDependencies(
                raw_channel=self._streaming.raw_channel,
                system_builder=self._builders.system,
                frame_packer=self._builders.packer,
            )
        ).jog_controller
        self.assertIsInstance(jog_ctrl, IJogController)
        self.assertFalse(jog_ctrl.jog('X', 5.0))
        self.assertFalse(jog_ctrl.set_feedrate_override(120))

    def test_tool_controller_contract(self) -> None:
        '''
            Tests ToolController satisfies IToolController structural protocol.

            :exceptions: None.
        '''
        tool_ctrl = ToolFactory.create(
            ToolDependencies(
                raw_channel=self._streaming.raw_channel,
                actuator_builder=self._builders.actuator,
                frame_packer=self._builders.packer,
            )
        ).tool_controller
        self.assertIsInstance(tool_ctrl, IToolController)
        self.assertIsInstance(tool_ctrl, IPurgeValveActuator)
        self.assertFalse(tool_ctrl.set_vacuum_pump(True))
        self.assertFalse(tool_ctrl.set_valve(True))
        self.assertFalse(tool_ctrl.pulse_purge_valve())

    def test_query_controller_contract(self) -> None:
        '''
            Tests QueryController satisfies IQueryController structural protocol.

            :exceptions: None.
        '''
        query_ctrl = QueryControllerFactory.create(
            QueryDependencies(
                raw_channel=self._streaming.raw_channel,
                system_builder=self._builders.system,
                frame_packer=self._builders.packer,
            )
        ).query_controller
        self.assertIsInstance(query_ctrl, IQueryController)
        self.assertFalse(query_ctrl.query_status())
        self.assertFalse(query_ctrl.query_position())


if __name__ == '__main__':
    main()
