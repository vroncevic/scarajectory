# -*- coding: UTF-8 -*-

'''
Module
    robot_response_dto.py
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
    Immutable Data Transfer Object for parsed robot firmware responses.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class RobotResponseDTO:
    '''
        Immutable data transfer object representing parsed microcontroller response.

        It defines:

            :attributes:
                | response_type - Category of response ('ACK', 'STATUS', 'DONE', 'ERR', 'FULL', 'UNKNOWN').
                | queue_depth - Reported remote buffer occupancy if available.
                | message - Informational or error description payload.
                | raw_line - Original unmodified text line received over transport.
                | is_success - False if error or full buffer condition reported.
    '''

    response_type: str
    queue_depth: int | None = None
    message: str = ''
    raw_line: str = ''
    is_success: bool = True
