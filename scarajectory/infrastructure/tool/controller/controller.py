# -*- coding: UTF-8 -*-

'''
Module
    controller.py
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

from typing import ClassVar, Final

from scaralang.core.model.protocol.frame import BinaryFrame
from scaralang.core.model.protocol.tool import ToolId
from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder

from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.tool.worker.irunner import IValvePulseRunner

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolController:
    '''
        Dedicated controller adapter for vacuum pump and purge valve actuation.

        It defines:

            :attributes:
                | PULSE_DELAY_SEC - ClassVar pulse delay duration in seconds.
                | _dispatcher - Injected IChannelDispatcher communication adapter.
                | _actuator_builder - Injected IBinaryActuatorFrameBuilder frame encoder.
                | _pulse_runner - Injected IValvePulseRunner collaborator.
            :methods:
                | __init__ - Initializes ToolController with dispatcher, builder, and runner.
                | is_connected - Checks if communication transport is active.
                | set_vacuum_pump - Sets end-effector vacuum pump state.
                | pulse_purge_valve - Pulses purge valve briefly to release vacuum suction.
                | deactivate_purge_valve - Concludes purge valve pulse deactivation.
                | set_valve - Sets purge valve state.
    '''

    PULSE_DELAY_SEC: ClassVar[float] = 0.3

    _dispatcher: IChannelDispatcher
    _actuator_builder: IBinaryActuatorFrameBuilder
    _pulse_runner: IValvePulseRunner

    def __init__(
        self,
        *,
        dispatcher: IChannelDispatcher,
        actuator_builder: IBinaryActuatorFrameBuilder,
        pulse_runner: IValvePulseRunner,
    ) -> None:
        '''
            Initializes ToolController with dispatcher, builder, and pulse runner.

            :param dispatcher: IChannelDispatcher transport and sequence manager.
            :param actuator_builder: IBinaryActuatorFrameBuilder builder instance.
            :param pulse_runner: Injected IValvePulseRunner collaborator.
            :exceptions: None.
        '''
        self._dispatcher: Final[IChannelDispatcher] = dispatcher
        self._actuator_builder: Final[IBinaryActuatorFrameBuilder] = actuator_builder
        self._pulse_runner: Final[IValvePulseRunner] = pulse_runner

    def is_connected(self) -> bool:
        '''
            Checks whether transport connection is currently active.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''
        return self._dispatcher.is_connected()

    def set_vacuum_pump(self, state: bool) -> bool:
        '''
            Sets end-effector vacuum pump state.

            :param state: True for ON, False for OFF.
            :return: True if command transmitted successfully, False otherwise.
            :exceptions: None.
        '''
        frame: BinaryFrame = self._actuator_builder.build_tool_cmd(
            seq_num=self._dispatcher.next_seq(),
            tool_id=int(ToolId.PUMP),
            state=state,
        )

        return self._dispatcher.send_frame(frame)

    def pulse_purge_valve(self) -> bool:
        '''
            Pulses purge valve briefly to release vacuum suction.

            :return: True if command transmitted successfully, False otherwise.
            :exceptions: None.
        '''
        if not self.is_connected():
            return False

        self.set_valve(True)
        self._pulse_runner.schedule_deactivation(
            actuator=self,
            delay_sec=self.PULSE_DELAY_SEC,
        )

        return True

    def deactivate_purge_valve(self) -> None:
        '''
            Deactivates purge valve if communication transport is connected.

            :exceptions: None.
        '''
        if self.is_connected():
            self.set_valve(False)

    def set_valve(self, state: bool) -> bool:
        '''
            Sets purge valve state.

            :param state: True for open, False for closed.
            :return: True if command transmitted successfully, False otherwise.
            :exceptions: None.
        '''
        frame: BinaryFrame = self._actuator_builder.build_tool_cmd(
            seq_num=self._dispatcher.next_seq(),
            tool_id=int(ToolId.VALVE),
            state=state,
        )

        return self._dispatcher.send_frame(frame)
