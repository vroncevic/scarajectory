# -*- coding: UTF-8 -*-

'''
Module
    validation_report.py
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
    Defines immutable ValidationReport data model holding trajectory validation results.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class ValidationReport:
    '''
        Immutable data model encapsulating trajectory plan kinematic validation results.

        It defines:

            :attributes:
                | is_valid - Flag indicating whether trajectory plan satisfies all kinematic constraints.
                | messages - Tuple of informative validation log messages.
                | errors - Tuple of critical kinematic violation messages.
                | warnings - Tuple of non-critical reachability advisory messages.
                | checked_points - Total count of verified trajectory waypoints.
    '''

    is_valid: bool
    messages: tuple[str, ...]
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    checked_points: int
