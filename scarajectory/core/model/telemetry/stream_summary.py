# -*- coding: UTF-8 -*-

'''
Module
    stream_summary.py
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
    Defines immutable StreamSummary data model encapsulating execution summary statistics.
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
class StreamSummary:
    '''
        Immutable data model encapsulating trajectory streaming session summary metrics.

        It defines:

            :attributes:
                | total_packets - Total number of packets in trajectory stream.
                | sent_packets - Number of transmitted packets.
                | acknowledged_packets - Number of successfully acknowledged packets.
                | failed_packets - Number of failed or unacknowledged packets.
                | elapsed_time_s - Total elapsed streaming time in seconds.
                | is_completed - Flag indicating if entire stream finished transmission.
    '''

    total_packets: int
    sent_packets: int
    acknowledged_packets: int
    failed_packets: int
    elapsed_time_s: float
    is_completed: bool
