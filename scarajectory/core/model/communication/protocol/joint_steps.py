# -*- coding: UTF-8 -*-

'''
Module
    joint_steps.py
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
    Defines JointSteps immutable value object for discrete joint step targets.
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
class JointSteps:
    '''
        Immutable joint step movement target and duration payload.

        It defines:

            :attributes:
                | target_j1_steps - Target step coordinate for Shoulder (J1).
                | target_j2_steps - Target step coordinate for Elbow (J2).
                | target_z_steps - Target step coordinate for Z-axis (Z).
                | target_j4_steps - Target step coordinate for Wrist (J4).
                | duration_us - Microsecond execution duration.
                | feedrate_scale - Feedrate speed scale factor.
    '''

    target_j1_steps: int
    target_j2_steps: int
    target_z_steps: int
    target_j4_steps: int
    duration_us: int
    feedrate_scale: int
