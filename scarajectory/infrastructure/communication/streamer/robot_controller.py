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
    Dedicated semantic robot controller adapter for immediate hardware actuation and diagnostics.
'''

from __future__ import annotations

from threading import Thread
from time import sleep
from typing import Final

from scarajectory.core.service.communication.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.infrastructure.communication.protocol.command_formatter import CommandFormatter

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
        Semantic robot controller executing immediate manual actuation commands.

        It defines:

            :attributes:
                | _streamer - Trajectory streamer used for transmitting ASCII protocol commands.
            :methods:
                | __init__ - Initializes the robot controller with injected streamer.
                | is_connected - Checks if communication transport is connected.
                | send_command - Transmits formatted command string if connected.
                | home - Executes robot homing routine.
                | enable - Energizes joint stepper motors.
                | disable - De-energizes joint stepper motors.
                | set_feedrate_override - Sets execution speed override percentage.
                | set_vacuum_pump - Sets end-effector vacuum pump state.
                | pulse_purge_valve - Pulses purge valve briefly to release vacuum suction.
                | set_valve - Sets purge valve state.
                | jog - Jogs specific robot axis by relative distance.
                | query_status - Queries microcontroller runtime status.
                | query_position - Queries current end-effector coordinates.
    '''

    _streamer: ITrajectoryStreamer

    def __init__(self, streamer: ITrajectoryStreamer) -> None:
        '''
            Initializes the robot controller with injected streamer.

            :param streamer: ITrajectoryStreamer instance.
        '''
        self._streamer: Final[ITrajectoryStreamer] = streamer

    def is_connected(self) -> bool:
        '''
            Checks whether communication transport is active.

            :return: True if connected, False otherwise.
        '''
        return self._streamer.is_connected()

    def send_command(self, cmd: str) -> bool:
        '''
            Transmits formatted command string if connected.

            :param cmd: Formatted command string.
            :return: True if transmitted, False if disconnected.
        '''
        if not self.is_connected():
            return False
        self._streamer.send_raw_command(cmd)
        return True

    def home(self) -> bool:
        '''
            Executes robot homing routine.

            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_home())

    def enable(self) -> bool:
        '''
            Energizes joint stepper motors.

            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_enable())

    def disable(self) -> bool:
        '''
            De-energizes joint stepper motors.

            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_disable())

    def set_feedrate_override(self, pct: int) -> bool:
        '''
            Sets execution speed override percentage.

            :param pct: Speed override percentage between 10 and 200.
            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_override(pct))

    def set_vacuum_pump(self, state: bool) -> bool:
        '''
            Sets end-effector vacuum pump state.

            :param state: True for ON, False for OFF.
            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_pump(state))

    def pulse_purge_valve(self) -> bool:
        '''
            Pulses purge valve briefly to release vacuum suction.

            :return: True if command transmitted successfully.
        '''
        if not self.is_connected():
            return False
        self.send_command(CommandFormatter.format_valve(True))
        Thread(target=self._delayed_valve_off, daemon=True).start()
        return True

    def _delayed_valve_off(self) -> None:
        '''
            Internal worker turning purge valve off after brief pulse.
        '''
        sleep(0.3)
        if self.is_connected():
            self.send_command(CommandFormatter.format_valve(False))

    def set_valve(self, state: bool) -> bool:
        '''
            Sets purge valve state.

            :param state: True for open, False for closed.
            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_valve(state))

    def jog(self, axis: str, step: float) -> bool:
        '''
            Jogs specific robot axis by relative distance.

            :param axis: Axis identifier ('X', 'Y', 'Z', 'Phi').
            :param step: Displacement step value.
            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_jog(axis, step))

    def query_status(self) -> bool:
        '''
            Queries microcontroller runtime status.

            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_status())

    def query_position(self) -> bool:
        '''
            Queries current end-effector coordinates.

            :return: True if command transmitted successfully.
        '''
        return self.send_command(CommandFormatter.format_getpos())
