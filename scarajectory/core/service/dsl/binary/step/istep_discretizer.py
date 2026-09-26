# -*- coding: UTF-8 -*-

'''
Module
    istep_discretizer.py
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
    Defines IStepDiscretizer Protocol for converting Cartesian waypoints to joint steps.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.protocol.joint_steps import JointSteps
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
class IStepDiscretizer(Protocol):
    '''
        Structural protocol defining joint step discretization and timing calculation.

        It defines:

            :methods:
                | discretize_waypoint - Solves IK and maps Cartesian waypoint into JointSteps.
                | calculate_segment_duration - Computes execution duration in microseconds.
    '''

    def discretize_waypoint(
        self,
        *,
        waypoint: Waypoint,
        prev_angles: tuple[float, float, float, float] | None = None
    ) -> tuple[JointSteps, tuple[float, float, float, float]]:
        '''
            Solves IK and converts Cartesian waypoint into motor steps with duration.

            :param waypoint: Target Cartesian Waypoint instance.
            :param prev_angles: Optional preceding joint angles in radians/mm.
            :return: Tuple of (JointSteps model, new joint angles tuple).
        '''

    def calculate_segment_duration(
        self,
        *,
        current_steps: tuple[int, int, int, int],
        target_steps: tuple[int, int, int, int],
        speed_mm_s: float
    ) -> int:
        '''
            Computes segment execution duration in microseconds.

            :param current_steps: Initial joint step coordinates.
            :param target_steps: Target joint step coordinates.
            :param speed_mm_s: Planned linear tool speed in mm/s.
            :return: Microsecond execution duration.
        '''
