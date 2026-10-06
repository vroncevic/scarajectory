# -*- coding: UTF-8 -*-

'''
Module
    manipulator_controllers_factory.py
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
    Factory instantiating and assembling manipulator sub-controllers.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scaralang.infrastructure.communication.protocol.binary.builder.binary_frame_builder_factory import BinaryFrameBuilderFactory
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.iraw_channel import IRawChannel
from scarajectory.infrastructure.gui.controls.manipulator_controllers_bundle import ManipulatorControllersBundle
from scarajectory.infrastructure.manipulator.jog_controller import JogController
from scarajectory.infrastructure.manipulator.jog_controller_factory import JogControllerFactory
from scarajectory.infrastructure.manipulator.motion_controller import MotionController
from scarajectory.infrastructure.manipulator.motion_controller_factory import MotionControllerFactory
from scarajectory.infrastructure.manipulator.query_controller import QueryController
from scarajectory.infrastructure.manipulator.query_controller_factory import QueryControllerFactory
from scarajectory.infrastructure.tool.tool_controller import ToolController
from scarajectory.infrastructure.tool.tool_controller_factory import ToolControllerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorControllersFactory:
    '''
        Factory instantiating and assembling manipulator sub-controllers.

        It defines:

            :methods:
                | create - Constructs manipulator sub-controllers.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        raw_channel: IRawChannel,
        *,
        protocol_mode: ProtocolMode = ProtocolMode.BINARY,
    ) -> ManipulatorControllersBundle:
        '''
            Constructs and bundles manipulator sub-controllers.

            :param raw_channel: Active communication channel.
            :param protocol_mode: Active communication protocol mode.
            :return: Assembled ManipulatorControllersBundle instance.
        '''
        frame_builder: IBinaryFrameBuilder = (
            BinaryFrameBuilderFactory.create()
        )
        motion_ctrl: MotionController = MotionControllerFactory.create(
            raw_channel=raw_channel,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )
        jog_ctrl: JogController = JogControllerFactory.create(
            raw_channel=raw_channel,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )
        tool_ctrl: ToolController = ToolControllerFactory.create(
            raw_channel=raw_channel,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )
        query_ctrl: QueryController = QueryControllerFactory.create(
            raw_channel=raw_channel,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )
        return ManipulatorControllersBundle(
            motion_ctrl=motion_ctrl,
            jog_ctrl=jog_ctrl,
            tool_ctrl=tool_ctrl,
            query_ctrl=query_ctrl,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
        '''
        return __version__
