# -*- coding: UTF-8 -*-

'''
Module
    tool_controller.py
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
    Dedicated controller adapter for vacuum pump and purge valve actuation.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.model.protocol.binary_frame import BinaryFrame
from scaralang.core.model.protocol.tool_id import ToolId
from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.connection.ichannel_dispatcher import IChannelDispatcher
from scarajectory.infrastructure.formatter.command_formatter import CommandFormatter
from scarajectory.infrastructure.tool.valve_pulse_worker import ValvePulseWorker
from scarajectory.infrastructure.tool.valve_pulse_worker_factory import ValvePulseWorkerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolController:
    '''
        Dedicated controller adapter for end-effector vacuum pump and purge valve actuation.

        It defines:

            :attributes:
                | _dispatcher - Injected IChannelDispatcher communication adapter.
                | _frame_builder - Injected IBinaryFrameBuilder frame encoder.
                | _worker_factory - Injected ValvePulseWorkerFactory class.
            :methods:
                | __init__ - Initializes ToolController with dispatcher and builder.
                | is_connected - Checks if communication transport is active.
                | set_protocol_mode - Updates protocol mode dynamically.
                | set_vacuum_pump - Sets end-effector vacuum pump state.
                | pulse_purge_valve - Pulses purge valve briefly to release vacuum suction.
                | deactivate_purge_valve - Concludes purge valve pulse deactivation.
                | set_valve - Sets purge valve state.
    '''

    _dispatcher: IChannelDispatcher
    _frame_builder: IBinaryFrameBuilder
    _worker_factory: type[ValvePulseWorkerFactory]

    def __init__(
        self,
        *,
        dispatcher: IChannelDispatcher,
        frame_builder: IBinaryFrameBuilder,
        worker_factory: type[ValvePulseWorkerFactory],
    ) -> None:
        '''
            Initializes ToolController with dispatcher, frame builder, and worker factory.

            :param dispatcher: IChannelDispatcher transport and sequence manager.
            :param frame_builder: IBinaryFrameBuilder builder instance.
            :param worker_factory: Injected ValvePulseWorkerFactory class.
            :exceptions: None.
        '''
        self._dispatcher: Final[IChannelDispatcher] = dispatcher
        self._frame_builder: Final[IBinaryFrameBuilder] = frame_builder
        self._worker_factory: Final[type[ValvePulseWorkerFactory]] = (
            worker_factory
        )

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
        '''
        return self._dispatcher.is_connected()

    def set_protocol_mode(self, mode: ProtocolMode) -> None:
        '''
            Updates active protocol mode dynamically.

            :param mode: ProtocolMode enum value.
        '''
        self._dispatcher.protocol_mode = mode

    def set_vacuum_pump(self, state: bool) -> bool:
        '''
            Sets end-effector vacuum pump state.

            :param state: True for ON, False for OFF.
            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._dispatcher.protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_tool_cmd(
                seq_num=self._dispatcher.next_seq(),
                tool_id=int(ToolId.PUMP),
                state=state,
            )

            return self._dispatcher.send_frame(frame)

        return self._dispatcher.send_command(CommandFormatter.format_pump(state))

    def pulse_purge_valve(self) -> bool:
        '''
            Pulses purge valve briefly to release vacuum suction.

            :return: True if command transmitted successfully, False otherwise.
        '''
        if not self.is_connected():
            return False

        self.set_valve(True)
        worker: ValvePulseWorker = self._worker_factory.create(
            delay_sec=0.3,
            actuator=self,
        )
        worker.start()

        return True

    def deactivate_purge_valve(self) -> None:
        '''
            Deactivates purge valve if communication transport is connected.
        '''
        if self.is_connected():
            self.set_valve(False)

    def set_valve(self, state: bool) -> bool:
        '''
            Sets purge valve state.

            :param state: True for open, False for closed.
            :return: True if command transmitted successfully, False otherwise.
        '''
        if self._dispatcher.protocol_mode == ProtocolMode.BINARY:
            frame: BinaryFrame = self._frame_builder.build_tool_cmd(
                seq_num=self._dispatcher.next_seq(),
                tool_id=int(ToolId.VALVE),
                state=state,
            )

            return self._dispatcher.send_frame(frame)

        return self._dispatcher.send_command(CommandFormatter.format_valve(state))
