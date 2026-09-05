# -*- coding: UTF-8 -*-

'''
Module
    scara_compiler_context.py
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
    Stateful context tracking robot state, coordinates, active frames, and pallets during compilation.
'''

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True)
class ScaraCompilerContext:
    '''
        Stateful compiler context tracking coordinate transformation, speeds, pallets, and pose.

        It defines:

            :attributes:
                | current_x - Current Cartesian X coordinate in mm.
                | current_y - Current Cartesian Y coordinate in mm.
                | current_z - Current Cartesian Z coordinate in mm.
                | current_phi - Current 4th axis tool orientation in degrees.
                | speed_rapid - Default rapid feedrate in mm/s.
                | speed_work - Default work feedrate in mm/s.
                | current_speed - Active motion feedrate in mm/s.
                | active_accel - Active path acceleration in mm/s^2.
                | elbow_config - Active elbow kinematic solution ('RIGHT' or 'LEFT').
                | frame_x - Active work frame X translation origin.
                | frame_y - Active work frame Y translation origin.
                | frame_angle_deg - Active work frame rotation angle in degrees.
                | tool_orient_mode - Tool orientation mode ('FIXED', 'TANGENTIAL', 'JOINT_LOCKED').
                | zone_mode - Corner transition mode ('FINE' or 'BLEND').
                | zone_radius - Corner blend radius in mm.
                | speed_override_pct - Global velocity scaling percentage (1-100).
                | pallets - Dictionary of defined pallet matrices.
            :methods:
                | transform_point - Transforms local frame (X, Y) into global world coordinates.
    '''

    current_x: float = 150.0
    current_y: float = 0.0
    current_z: float = 20.0
    current_phi: float = 0.0
    speed_rapid: float = 150.0
    speed_work: float = 40.0
    current_speed: float = 40.0
    active_accel: float = 300.0
    elbow_config: str = 'RIGHT'
    frame_x: float = 0.0
    frame_y: float = 0.0
    frame_angle_deg: float = 0.0
    tool_orient_mode: str = 'FIXED'
    zone_mode: str = 'FINE'
    zone_radius: float = 0.0
    speed_override_pct: float = 100.0
    pallets: dict[str, dict[str, Any]] = field(default_factory=dict)

    def transform_point(self, *, x: float, y: float) -> tuple[float, float]:
        '''
            Transforms point (x, y) from active local frame to global base coordinate system.

            :param x: Local X coordinate.
            :param y: Local Y coordinate.
            :return: Tuple of transformed (global_x, global_y).
        '''
        if (
            self.frame_x == 0.0
            and self.frame_y == 0.0
            and self.frame_angle_deg == 0.0
        ):
            return x, y

        import math

        rad = math.radians(self.frame_angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        gx = self.frame_x + (x * cos_a - y * sin_a)
        gy = self.frame_y + (x * sin_a + y * cos_a)
        return gx, gy
