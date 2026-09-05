# -*- coding: UTF-8 -*-

'''
Module
    scara_plan_exporter.py
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
    Implementation of trajectory plan exporter converting waypoints into SCARA DSL code.
'''

from __future__ import annotations

from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaraPlanExporter:
    '''
        Exports active TrajectoryPlan waypoints into clean, readable SCARA DSL source text.

        It defines:

            :methods:
                | export_plan - Serializes trajectory plan into formatted .scara source code.
    '''

    def export_plan(self, plan: ITrajectoryPlan) -> str:
        '''
            Serializes trajectory plan into formatted .scara source code.

            :param plan: Trajectory plan instance.
            :return: Formatted SCARA DSL script.
            :exceptions: None.
        '''
        waypoints: tuple[Waypoint, ...] = plan.waypoints
        if not waypoints:
            return '# SCARAjectory DSL Program\n# Empty trajectory plan\n'

        lines: list[str] = [
            '# ==========================================================',
            '# SCARAjectory DSL Program',
            f'# Generated with {len(waypoints)} waypoints',
            '# ==========================================================',
            'CONFIG ELBOW RIGHT',
            'SPEED RAPID 100.0',
            f'SPEED WORK {waypoints[0].speed:.1f}',
            'ACCEL 500.0',
            'ZONE FINE',
            '',
        ]

        # First waypoint is typically approached via rapid PTP move
        first: Waypoint = waypoints[0]
        first_comment = f'  # {first.name}' if first.name else ''
        lines.append(
            f'MOVE_J X={first.x:.2f} Y={first.y:.2f} Z={first.z:.2f} PHI={first.phi:.2f}{first_comment}'
        )

        # Subsequent waypoints use linear moves
        for pt in waypoints[1:]:
            comment = f'  # {pt.name}' if pt.name else ''
            lines.append(
                f'MOVE_L X={pt.x:.2f} Y={pt.y:.2f} Z={pt.z:.2f} PHI={pt.phi:.2f} SPEED={pt.speed:.1f}{comment}'
            )

        lines.append('')
        return '\n'.join(lines)
