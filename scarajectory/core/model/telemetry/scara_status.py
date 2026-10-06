# -*- coding: UTF-8 -*-

'''
Module
    scara_status.py
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
    Defines ScaraStatus value object representing telemetry and state.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ScaraStatus:
    '''
        Immutable telemetry snapshot of robot state, motion, and coordinates.

        It defines:

            :attributes:
                | system_state - High-level system state (0=IDLE, 1=RUNNING, 2=HOLD, 3=ESTOP).
                | is_busy - Motion execution flag.
                | queue_count - Pending motion segment count in firmware buffer.
                | j1_steps - Current accumulated shoulder steps.
                | j2_steps - Current accumulated elbow steps.
                | z_steps - Current accumulated Z-axis steps.
                | j4_steps - Current accumulated wrist steps.
    '''

    system_state: int
    is_busy: bool
    queue_count: int
    j1_steps: int
    j2_steps: int
    z_steps: int
    j4_steps: int
