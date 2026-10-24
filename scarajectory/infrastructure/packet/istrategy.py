# -*- coding: UTF-8 -*-

'''
Module
    istrategy.py
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
    Defines structural protocol IPacketStrategy for waypoint packet formatting.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPacketStrategy(Protocol):
    '''
        Structural protocol defining waypoint packet formatting strategy.

        It defines:

            :methods:
                | format_waypoint_packet - Formats waypoint entity into wire transmission payload bytes.
                | reset - Resets internal kinematic angle tracking state to home position.
                | get_version - Returns component version string.
    '''

    def format_waypoint_packet(
        self,
        *,
        waypoint: TrajectoryWaypoint,
        seq_num: int = 0,
    ) -> bytes:
        '''
            Formats waypoint entity into wire transmission payload bytes.

            :param waypoint: Target waypoint entity to encode.
            :param seq_num: Packet cyclic sequence number (0-255).
            :return: Encoded packet bytes for transmission.
        '''

    def reset(self) -> None:
        '''
            Resets internal kinematic angle tracking state to home position.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
        '''
