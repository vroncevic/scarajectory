# -*- coding: UTF-8 -*-

'''
Module
    robot_controller.py
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
    Composite hardware adapter facade orchestrating motion, jogging, tool, and query controllers.
'''

from __future__ import annotations

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.service.communication.stream.iraw_channel import IRawChannel
from scarajectory.infrastructure.communication.controller.jog_controller import JogController
from scarajectory.infrastructure.communication.controller.motion_controller import MotionController
from scarajectory.infrastructure.communication.controller.query_controller import QueryController
from scarajectory.infrastructure.communication.controller.tool_controller import ToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class RobotController:
    '''
        Composite hardware adapter facade orchestrating motion, jogging, tool, and query controllers.

        It defines:

            :attributes:
                | _motion_controller - Sub-controller handling homing and motor power.
                | _jog_controller - Sub-controller handling manual jog and override.
                | _tool_controller - Sub-controller handling vacuum and purge valve.
                | _query_controller - Sub-controller handling telemetry and status queries.
                | _streamer - Streamer transport reference for raw comms and connectivity.
                | _frame_builder - Binary frame encoder reference for raw wire transmission.
                | _protocol_mode - Active wire protocol mode enum value.

            :methods:
                | is_connected - Checks whether communication transport is active.
                | set_protocol_mode - Updates protocol mode dynamically across all controllers.
                | send_command - Transmits formatted command string if connected.
                | send_binary_frame - Packs and transmits binary frame if connected.
                | home - Delegates homing execution to MotionController.
                | enable - Delegates stepper motor power-on to MotionController.
                | disable - Delegates stepper motor power-off to MotionController.
                | clear_fault - Delegates fault latch clearance to MotionController.
                | jog - Delegates axis jog to JogController.
                | set_feedrate_override - Delegates speed override to JogController.
                | set_vacuum_pump - Delegates vacuum pump actuation to ToolController.
                | pulse_purge_valve - Delegates vacuum purge pulse to ToolController.
                | set_valve - Delegates purge valve actuation to ToolController.
                | query_status - Delegates status query to QueryController.
                | query_position - Delegates position query to QueryController.
                | get_motion_controller - Returns internal MotionController instance.
                | get_jog_controller - Returns internal JogController instance.
                | get_tool_controller - Returns internal ToolController instance.
                | get_query_controller - Returns internal QueryController instance.
    '''

    _motion_controller: MotionController
    _jog_controller: JogController
    _tool_controller: ToolController
    _query_controller: QueryController
    _raw_channel: IRawChannel
    _frame_builder: IBinaryFrameBuilder
    _protocol_mode: ProtocolMode

    def __init__(
        self,
        motion_controller: MotionController,
        jog_controller: JogController,
        tool_controller: ToolController,
        query_controller: QueryController,
        raw_channel: IRawChannel,
        frame_builder: IBinaryFrameBuilder,
        protocol_mode: ProtocolMode,
    ) -> None:
        '''
            Initializes composite RobotController facade with delegated controllers and transport.

            :param motion_controller: MotionController instance.
            :param jog_controller: JogController instance.
            :param tool_controller: ToolController instance.
            :param query_controller: QueryController instance.
            :param raw_channel: IRawChannel instance.
            :param frame_builder: IBinaryFrameBuilder instance.
            :param protocol_mode: Active ProtocolMode enum value.
        '''
        self._motion_controller = motion_controller
        self._jog_controller = jog_controller
        self._tool_controller = tool_controller
        self._query_controller = query_controller
        self._raw_channel = raw_channel
        self._frame_builder = frame_builder
        self._protocol_mode = protocol_mode

    def is_connected(self) -> bool:
        '''
            Checks whether communication transport is active.

            :return: True if connected, False otherwise.
        '''
        return self._raw_channel.is_connected()

    def set_protocol_mode(self, mode: ProtocolMode) -> None:
        '''
            Updates protocol mode dynamically across facade and sub-controllers.

            :param mode: ProtocolMode enum value.
        '''
        self._protocol_mode = mode
        self._motion_controller.set_protocol_mode(mode)
        self._jog_controller.set_protocol_mode(mode)
        self._tool_controller.set_protocol_mode(mode)
        self._query_controller.set_protocol_mode(mode)

    def send_command(self, cmd: str) -> bool:
        '''
            Transmits formatted command string if connected.

            :param cmd: Formatted command string.
            :return: True if transmitted, False if disconnected.
        '''
        if not self.is_connected():
            return False
    
        self._raw_channel.send_raw_command(cmd)
    
        return True

    def send_binary_frame(self, frame: BinaryFrame) -> bool:
        '''
            Packs and transmits binary frame if connected.

            :param frame: BinaryFrame instance.
            :return: True if transmitted, False otherwise.
        '''
        if not self.is_connected():
            return False

        payload_bytes: bytes = self._frame_builder.pack_frame(frame=frame)

        return self._raw_channel.send_raw_bytes(payload_bytes)

    def home(self) -> bool:
        '''
            Executes robot homing routine via MotionController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._motion_controller.home()

    def enable(self) -> bool:
        '''
            Energizes joint stepper motors via MotionController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._motion_controller.enable()

    def disable(self) -> bool:
        '''
            De-energizes joint stepper motors via MotionController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._motion_controller.disable()

    def clear_fault(self) -> bool:
        '''
            Clears latched hardware fault state via MotionController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._motion_controller.clear_fault()

    def jog(self, axis: str, step: float) -> bool:
        '''
            Jogs specific robot axis via JogController.

            :param axis: Axis identifier string ('X', 'Y', 'Z', 'Phi', etc.).
            :param step: Relative displacement step value.
            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._jog_controller.jog(axis, step)

    def set_feedrate_override(self, pct: int) -> bool:
        '''
            Sets execution speed override percentage via JogController.

            :param pct: Speed override percentage between 10 and 200.
            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._jog_controller.set_feedrate_override(pct)

    def set_vacuum_pump(self, state: bool) -> bool:
        '''
            Sets end-effector vacuum pump state via ToolController.

            :param state: True for ON, False for OFF.
            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._tool_controller.set_vacuum_pump(state)

    def pulse_purge_valve(self) -> bool:
        '''
            Pulses purge valve briefly via ToolController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._tool_controller.pulse_purge_valve()

    def set_valve(self, state: bool) -> bool:
        '''
            Sets purge valve state via ToolController.

            :param state: True for open, False for closed.
            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._tool_controller.set_valve(state)

    def query_status(self) -> bool:
        '''
            Queries microcontroller runtime status via QueryController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._query_controller.query_status()

    def query_position(self) -> bool:
        '''
            Queries current end-effector coordinates via QueryController.

            :return: True if command transmitted successfully, False otherwise.
        '''
        return self._query_controller.query_position()

    def get_motion_controller(self) -> MotionController:
        '''
            Returns internal MotionController instance.

            :return: MotionController instance.
        '''
        return self._motion_controller

    def get_jog_controller(self) -> JogController:
        '''
            Returns internal JogController instance.

            :return: JogController instance.
        '''
        return self._jog_controller

    def get_tool_controller(self) -> ToolController:
        '''
            Returns internal ToolController instance.

            :return: ToolController instance.
        '''
        return self._tool_controller

    def get_query_controller(self) -> QueryController:
        '''
            Returns internal QueryController instance.

            :return: QueryController instance.
        '''
        return self._query_controller
