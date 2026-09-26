# -*- coding: UTF-8 -*-

'''
Module
    iwaypoint_factory.py
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
    Structural protocol interface for Waypoint domain model factory providers.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IWaypointFactory(Protocol):
    '''
        Protocol defining factory operations for constructing Waypoint entities.

        It defines:

            :methods:
                | create - Constructs and returns an immutable Waypoint domain entity.
    '''

    def create(
        self,
        *,
        x: float,
        y: float,
        z: float,
        speed: float,
        phi: float = 0.0,
        name: str = '',
        command: str = '',
    ) -> Waypoint:
        '''
            Constructs and returns an immutable Waypoint domain entity.

            :param x: X Cartesian coordinate in mm.
            :param y: Y Cartesian coordinate in mm.
            :param z: Z height coordinate in mm.
            :param speed: Motion feedrate speed in mm/s.
            :param phi: Tool orientation angle in degrees.
            :param name: Optional waypoint identifier.
            :param command: Optional protocol command string.
            :return: Fully configured Waypoint domain entity.
            :exceptions: None.
        '''
        ...
