# -*- coding: UTF-8 -*-

'''
Module
    stream_state.py
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
    Defines StreamState enumeration for motion streaming status.
'''

from __future__ import annotations

from enum import Enum, auto

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamState(Enum):
    '''
        State of the serial streaming process.

        It defines:

            :attributes:
                | IDLE - Streamer is idle.
                | STREAMING - Waypoints are being transmitted.
                | PAUSED - Transmission is paused.
                | STOPPED - Transmission was stopped or aborted.
                | COMPLETED - Trajectory transmission completed successfully.
                | ERROR - Error occurred during streaming.
    '''

    IDLE = auto()
    STREAMING = auto()
    PAUSED = auto()
    STOPPED = auto()
    COMPLETED = auto()
    ERROR = auto()
