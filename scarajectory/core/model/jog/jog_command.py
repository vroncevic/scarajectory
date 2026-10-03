# -*- coding: UTF-8 -*-

'''
Module
    jog_command.py
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
    Defines immutable JogCommand data model representing an incremental motion request.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.jog.jog_axis import JogAxis
from scarajectory.core.model.jog.jog_direction import JogDirection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class JogCommand:
    '''
        Immutable data model encapsulating a manual jog displacement command.

        It defines:

            :attributes:
                | axis - Target robot kinematic axis to displace.
                | direction - Positive or negative displacement direction.
                | step_mm - Step displacement distance in millimeters or degrees.
                | feedrate - Movement velocity in millimeters per second.
    '''

    axis: JogAxis
    direction: JogDirection
    step_mm: float
    feedrate: float
