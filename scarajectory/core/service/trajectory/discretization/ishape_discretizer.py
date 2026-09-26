# -*- coding: UTF-8 -*-

'''
Module
    ishape_discretizer.py
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
    Defines IShapeDiscretizer protocol for geometric CAD shape discretization.
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
class IShapeDiscretizer(Protocol):
    '''
        Protocol defining contract for discretizing 2D geometric shapes into waypoints.

        It defines:

            :methods:
                | discretize_line - Discretizes straight linear segment.
                | discretize_circle - Discretizes circular boundary into polygonal waypoints.
                | discretize_rectangle - Discretizes rectangular boundary into corner waypoints.
    '''

    def discretize_line(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Generates start and end waypoints of straight linear segment.

            :param p1: Start coordinate (x, y) tuple in mm.
            :param p2: End coordinate (x, y) tuple in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: List of Waypoint instances.
        '''

    def discretize_circle(
        self,
        center: tuple[float, float],
        radius: float,
        steps: int,
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Generates circle perimeter waypoints.

            :param center: Center coordinate (x, y) tuple in mm.
            :param radius: Circle radius in mm.
            :param steps: Discretization step count.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: List of Waypoint instances.
        '''

    def discretize_rectangle(
        self,
        p1: tuple[float, float],
        p2: tuple[float, float],
        *,
        z: float,
        speed: float,
    ) -> list[Waypoint]:
        '''
            Generates corner waypoints of closed rectangular boundary.

            :param p1: Initial corner coordinate (x, y) tuple in mm.
            :param p2: Opposite corner coordinate (x, y) tuple in mm.
            :param z: Z vertical height coordinate in mm.
            :param speed: Feedrate speed in mm/s.
            :return: List of Waypoint instances.
        '''
