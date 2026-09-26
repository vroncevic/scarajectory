# -*- coding: UTF-8 -*-

'''
Module
    program.py
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
    Defines immutable Program model representing compiled binary stream payload.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.dsl.binary.step import Step

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class Program:
    '''
        Compiled binary program payload container.

        It defines:

        :attributes:
            | steps - Tuple of binary execution steps.
            | raw_bytes - Packed byte sequence for wire streaming.
            | total_duration_us - Total estimated execution duration in microseconds.
            | instruction_count - Total number of compiled instructions.
            | step_counts - Tuple of step counts per joint axis.
    '''

    steps: tuple[Step, ...]
    raw_bytes: bytes
    total_duration_us: int
    instruction_count: int
    step_counts: tuple[int, ...]
