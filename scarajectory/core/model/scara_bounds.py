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
__version__ = '1.0.0'
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
    '''

    l1: float = 150.0
    l2: float = 120.0
    z_min: float = 0.0
    z_max: float = 100.0
    min_speed: float = 1.0
    max_speed: float = 100.0
