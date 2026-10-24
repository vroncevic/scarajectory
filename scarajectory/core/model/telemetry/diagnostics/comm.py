# -*- coding: UTF-8 -*-

'''
Module
    comm.py
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
    Defines CommunicationsDiagnostics domain model encapsulating UART and buffer metrics.
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
class CommunicationsDiagnostics:
    '''
        Domain model encapsulating UART frames, error counters, and buffer metrics.

        It defines:

            :attributes:
                | rx_frames_total - Total frames received by MCU.
                | tx_frames_total - Total frames transmitted by MCU.
                | crc_errors - Total CRC checksum failure count.
                | rx_buffer_overruns - Total buffer overrun count.
                | queue_high_watermark - Peak instruction queue depth.
                | mem_pool_min_free - Minimum free memory pool bytes observed.
                | uptime_ms - Monotonic firmware uptime in milliseconds.
    '''

    rx_frames_total: int
    tx_frames_total: int
    crc_errors: int
    rx_buffer_overruns: int
    queue_high_watermark: int
    mem_pool_min_free: int
    uptime_ms: int
