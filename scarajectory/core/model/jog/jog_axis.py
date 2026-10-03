# -*- coding: UTF-8 -*-

'''
Module
    jog_axis.py
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
    Defines JogAxis enumeration representing controllable robot axes.
'''

from __future__ import annotations

from enum import StrEnum, unique

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@unique
class JogAxis(StrEnum):
    '''
        Controllable robot kinematic axes for manual jog motion.

        It defines:

            :values:
                | X - Primary horizontal Cartesian X translation axis.
                | Y - Secondary horizontal Cartesian Y translation axis.
                | Z - Vertical Cartesian Z elevation axis.
                | PHI - End-effector wrist orientation rotation axis.
    '''

    X = 'X'
    Y = 'Y'
    Z = 'Z'
    PHI = 'PHI'
