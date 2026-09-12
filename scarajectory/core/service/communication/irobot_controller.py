# -*- coding: UTF-8 -*-

'''
Module
    irobot_controller.py
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
    Defines IRobotController port interface for high-level semantic robot actuation.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IRobotController(Protocol):
    '''
        Semantic robot controller port for high-level hardware operations.

        It defines:

            :methods:
                | home - Executes robot homing sequence.
                | enable - Energizes and enables joint stepper motors.
                | disable - De-energizes joint stepper motors.
                | set_feedrate_override - Sets execution speed override percentage.
                | set_vacuum_pump - Turns end-effector vacuum pump on or off.
                | pulse_purge_valve - Pulses purge valve briefly to release vacuum.
                | set_valve - Sets end-effector purge valve state.
                | jog - Jogs specific axis by relative distance.
                | query_status - Queries runtime hardware status.
                | query_position - Queries current end-effector position.
    '''

    def home(self) -> bool:
        '''
            Executes robot homing sequence.

            :return: True if command transmitted successfully.
        '''

    def enable(self) -> bool:
        '''
            Energizes and enables joint stepper motors.

            :return: True if command transmitted successfully.
        '''

    def disable(self) -> bool:
        '''
            De-energizes joint stepper motors.

            :return: True if command transmitted successfully.
        '''

    def set_feedrate_override(self, pct: int) -> bool:
        '''
            Sets execution speed override percentage.

            :param pct: Speed override percentage between 10 and 200.
            :return: True if command transmitted successfully.
        '''

    def set_vacuum_pump(self, state: bool) -> bool:
        '''
            Turns end-effector vacuum pump on or off.

            :param state: True for ON, False for OFF.
            :return: True if command transmitted successfully.
        '''

    def pulse_purge_valve(self) -> bool:
        '''
            Pulses purge valve briefly to release vacuum.

            :return: True if command transmitted successfully.
        '''

    def set_valve(self, state: bool) -> bool:
        '''
            Sets end-effector purge valve state.

            :param state: True for open, False for closed.
            :return: True if command transmitted successfully.
        '''

    def jog(self, axis: str, step: float) -> bool:
        '''
            Jogs specific axis by relative distance.

            :param axis: Axis name ('X', 'Y', 'Z', 'Phi').
            :param step: Displacement in mm or degrees.
            :return: True if command transmitted successfully.
        '''

    def query_status(self) -> bool:
        '''
            Queries runtime hardware status.

            :return: True if command transmitted successfully.
        '''

    def query_position(self) -> bool:
        '''
            Queries current end-effector position.

            :return: True if command transmitted successfully.
        '''
