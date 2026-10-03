# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_snapshot.py
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
    Defines DiagnosticsSnapshot domain model representing firmware diagnostic telemetry.
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
class DiagnosticsSnapshot:
    '''
        Domain model representing comprehensive firmware diagnostics report.

        It defines:

            :attributes:
                | rx_frames_total - Total received binary frames count.
                | tx_frames_total - Total transmitted binary frames count.
                | crc_errors - Total CRC checksum mismatch errors encountered.
                | rx_buffer_overruns - Total UART receive FIFO overruns.
                | queue_high_watermark - Peak ring buffer queue occupancy.
                | mem_pool_min_free - Minimum available block allocations.
                | total_steps_executed_j1 - Monotonic executed steps for joint 1.
                | total_steps_executed_j2 - Monotonic executed steps for joint 2.
                | total_steps_executed_z - Monotonic executed steps for Z axis.
                | total_steps_executed_j4 - Monotonic executed steps for wrist joint 4.
                | following_error_j1 - Real-time tracking error for joint 1 in steps.
                | following_error_j2 - Real-time tracking error for joint 2 in steps.
                | following_error_z - Real-time tracking error for Z axis in steps.
                | following_error_j4 - Real-time tracking error for joint 4 in steps.
                | stall_guard_flags - Stepper driver stall detection bitmask flags.
                | driver_fault_flags - Hardware driver fault status bitmask flags.
                | uptime_ms - Monotonic microcontroller system uptime in milliseconds.
    '''

    rx_frames_total: int
    tx_frames_total: int
    crc_errors: int
    rx_buffer_overruns: int
    queue_high_watermark: int
    mem_pool_min_free: int
    total_steps_executed_j1: int
    total_steps_executed_j2: int
    total_steps_executed_z: int
    total_steps_executed_j4: int
    following_error_j1: int
    following_error_j2: int
    following_error_z: int
    following_error_j4: int
    stall_guard_flags: int
    driver_fault_flags: int
    uptime_ms: int
