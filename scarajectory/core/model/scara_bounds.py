# -*- coding: UTF-8 -*-

'''
Module
    scara_bounds.py
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
    Defines ScaraBounds domain value object for kinematic limits.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraBounds:
    '''
        Domain Value Object encapsulating kinematic geometry and operational limits for SCARA arm.

        It defines:

            :attributes:
                | l1 - Length of primary SCARA link in mm.
                | l2 - Length of secondary SCARA link in mm.
                | z_min - Minimum vertical height limit in mm.
                | z_max - Maximum vertical height limit in mm.
                | min_speed - Minimum feedrate speed limit in mm/s.
                | max_speed - Maximum feedrate speed limit in mm/s.
                | default_speed - Default Cartesian linear speed in mm/s.
                | default_accel - Default acceleration in mm/s^2.
                | max_accel - Maximum acceleration in mm/s^2.
                | j1_min_rad - Joint 1 (Shoulder) minimum angle in radians.
                | j1_max_rad - Joint 1 (Shoulder) maximum angle in radians.
                | j2_min_rad - Joint 2 (Elbow) minimum angle in radians.
                | j2_max_rad - Joint 2 (Elbow) maximum angle in radians.
                | singularity_outer_margin_mm - Outer reach safety margin in mm.
                | singularity_inner_margin_mm - Inner reach safety margin in mm.
                | singularity_theta2_min_rad - Elbow singularity deadband in radians.
                | deadzone_r_min - Inner deadzone radius due to folded elbow in mm.
    '''

    l1: float = 150.0
    l2: float = 120.0
    z_min: float = 0.0
    z_max: float = 100.0
    min_speed: float = 1.0
    max_speed: float = 250.0
    default_speed: float = 50.0
    default_accel: float = 300.0
    max_accel: float = 2000.0
    j1_min_rad: float = -2.617994
    j1_max_rad: float = 2.617994
    j2_min_rad: float = -2.530727
    j2_max_rad: float = 2.530727
    singularity_outer_margin_mm: float = 3.0
    singularity_inner_margin_mm: float = 3.0
    singularity_theta2_min_rad: float = 0.087266
    deadzone_r_min: float = 86.08
