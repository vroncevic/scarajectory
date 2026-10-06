# -*- coding: UTF-8 -*-

'''
Module
    tool_controller_factory.py
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
    Factory service constructing ToolController semantic adapters.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.infrastructure.connection.ichannel_dispatcher import IChannelDispatcher
from scarajectory.infrastructure.connection.iraw_channel import IRawChannel
from scarajectory.infrastructure.connection.channel_dispatcher_factory import ChannelDispatcherFactory
from scarajectory.infrastructure.tool.tool_controller import ToolController
from scarajectory.infrastructure.tool.valve_pulse_worker_factory import ValvePulseWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolControllerFactory:
    '''
        Factory providing creation of ToolController semantic adapters.

        It defines:

            :methods:
                | create - Constructs ToolController with injected streamer and frame builder.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        raw_channel: IRawChannel,
        frame_builder: IBinaryFrameBuilder,
        *,
        protocol_mode: ProtocolMode = ProtocolMode.ASCII,
    ) -> ToolController:
        '''
            Constructs and returns a ToolController instance.

            :param raw_channel: IRawChannel instance.
            :param frame_builder: IBinaryFrameBuilder instance.
            :param protocol_mode: Active ProtocolMode enum value.
            :return: Configured ToolController instance.
        '''
        dispatcher: IChannelDispatcher = ChannelDispatcherFactory.create(
            raw_channel=raw_channel,
            frame_builder=frame_builder,
            protocol_mode=protocol_mode,
        )

        return ToolController(
            dispatcher=dispatcher,
            frame_builder=frame_builder,
            worker_factory=ValvePulseWorkerFactory,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
        '''
        return __version__
