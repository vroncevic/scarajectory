# -*- coding: UTF-8 -*-

'''
Module
    stream_progress.py
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
    Defines StreamProgress metric container for streaming progress updates.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.stream_state import StreamState

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True, kw_only=True)
class StreamProgress:
    '''
        Progress metrics during trajectory streaming.

        It defines:

            :attributes:
                | state - Current StreamState enum value.
                | total_waypoints - Total number of waypoints to stream.
                | sent_waypoints - Number of waypoints sent to robot.
                | completed_waypoints - Number of waypoints confirmed completed.
                | current_line - Currently executing packet line.
                | error_message - Error description if any.
                | elapsed_seconds - Elapsed time in seconds.
            :methods:
                | percentage - Calculates completion percentage from 0.0 to 100.0.
    '''

    state: StreamState
    total_waypoints: int
    sent_waypoints: int
    completed_waypoints: int
    failed_waypoints: int = 0
    current_line: str = ''
    error_message: str = ''
    elapsed_seconds: float = 0.0

    @property
    def percentage(self) -> float:
        '''
            Calculates completion percentage from 0.0 to 100.0.

            :return: Percentage of completion.
            :exceptions: None.
        '''
        if self.total_waypoints == 0:
            return 0.0
        return ((self.completed_waypoints + self.failed_waypoints) / self.total_waypoints) * 100.0
