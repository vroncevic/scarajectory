# -*- coding: UTF-8 -*-

'''
Module
    transmission_parameters.py
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
    Defines TransmissionParameters domain value object for motor and gear configuration.
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
class TransmissionParameters:
    '''
        Domain Value Object encapsulating motor resolution and transmission gear ratios.

        It defines:

            :attributes:
                | steps_per_rev - Base steps per motor revolution (e.g. 200).
                | microstepping - Stepper driver microstepping division (e.g. 16).
                | gear_ratio_j1 - Pulley reduction ratio for Shoulder (J1).
                | gear_ratio_j2 - Pulley reduction ratio for Elbow (J2).
                | gear_ratio_j4 - Reduction ratio for Wrist (J4).
                | leadscrew_pitch_z - Z-axis leadscrew pitch in mm/rev (e.g. 8.0).
    '''

    steps_per_rev: float
    microstepping: float
    gear_ratio_j1: float
    gear_ratio_j2: float
    gear_ratio_j4: float
    leadscrew_pitch_z: float
