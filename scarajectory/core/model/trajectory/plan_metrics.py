# -*- coding: UTF-8 -*-

'''
Module
    plan_metrics.py
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
    Defines immutable PlanMetrics data model holding computed trajectory statistics.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class PlanMetrics:
    '''
        Immutable data model encapsulating computed trajectory path metrics.

        It defines:

            :attributes:
                | total_points - Number of discrete waypoints in trajectory plan.
                | total_length_mm - Cumulative Cartesian path distance in millimeters.
                | estimated_time_s - Estimated total motion execution duration in seconds.
                | min_speed - Minimum programmed velocity across path in mm/s.
                | max_speed - Maximum programmed velocity across path in mm/s.
    '''

    total_points: int
    total_length_mm: float
    estimated_time_s: float
    min_speed: float
    max_speed: float
