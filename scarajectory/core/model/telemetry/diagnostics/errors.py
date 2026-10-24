# -*- coding: UTF-8 -*-

'''
Module
    errors.py
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
    Defines FollowingErrorsDiagnostics domain model encapsulating tracking errors.
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
class FollowingErrorsDiagnostics:
    '''
        Domain model encapsulating real-time closed-loop following tracking error in steps.

        It defines:

            :attributes:
                | j1 - Real-time tracking error for joint 1 in steps.
                | j2 - Real-time tracking error for joint 2 in steps.
                | z - Real-time tracking error for Z vertical axis in steps.
                | j4 - Real-time tracking error for wrist joint 4 in steps.
    '''

    j1: int
    j2: int
    z: int
    j4: int
