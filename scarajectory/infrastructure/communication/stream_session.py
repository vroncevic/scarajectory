# -*- coding: UTF-8 -*-

'''
Module
    stream_session.py
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
    Internal streaming session data model tracking waypoints and progress metrics.
'''

from __future__ import annotations

from dataclasses import dataclass, field

from scarajectory.core.model.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True)
class StreamSession:
    '''
        Mutable state container tracking active stream counters and remote queue capacity.

        It defines:

            :attributes:
                | waypoints - List of active waypoints being streamed.
                | sent_count - Number of waypoints transmitted to microcontroller.
                | done_count - Number of waypoints confirmed executed.
                | remote_queue_depth - Current buffer occupancy on microcontroller.
                | start_time - Timestamp when stream execution started.
    '''

    waypoints: list[Waypoint] = field(default_factory=list)
    sent_count: int = 0
    done_count: int = 0
    failed_count: int = 0
    remote_queue_depth: int = 0
    start_time: float = 0.0
