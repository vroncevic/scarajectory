# -*- coding: UTF-8 -*-

'''
Module
    steps.py
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
    Defines JointStepsDiagnostics domain model encapsulating executed axis steps.
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
class JointStepsDiagnostics:
    '''
        Domain model encapsulating monotonic step counts executed on each joint axis.

        It defines:

            :attributes:
                | j1 - Monotonic executed steps for joint 1.
                | j2 - Monotonic executed steps for joint 2.
                | z - Monotonic executed steps for Z vertical axis.
                | j4 - Monotonic executed steps for wrist joint 4.
    '''

    j1: int
    j2: int
    z: int
    j4: int
