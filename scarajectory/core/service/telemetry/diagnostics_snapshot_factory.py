# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_snapshot_factory.py
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
    Factory service constructing DiagnosticsSnapshot models.
'''

from __future__ import annotations

from scarajectory.core.model.telemetry.diagnostics_bundle import DiagnosticsBundle
from scarajectory.core.model.telemetry.diagnostics_snapshot import DiagnosticsSnapshot

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsSnapshotFactory:
    '''
        Factory service constructing DiagnosticsSnapshot models.

        It defines:

            :methods:
                | create - Constructs DiagnosticsSnapshot model with explicit parameters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, *, bundle: DiagnosticsBundle) -> DiagnosticsSnapshot:
        '''
            Constructs DiagnosticsSnapshot model instance from telemetry bundle.

            :param bundle: DiagnosticsBundle containing telemetry parameters.
            :return: DiagnosticsSnapshot model instance.
        '''
        return DiagnosticsSnapshot(
            rx_frames_total=bundle.rx_frames_total,
            tx_frames_total=bundle.tx_frames_total,
            crc_errors=bundle.crc_errors,
            rx_buffer_overruns=bundle.rx_buffer_overruns,
            queue_high_watermark=bundle.queue_high_watermark,
            mem_pool_min_free=bundle.mem_pool_min_free,
            total_steps_executed_j1=bundle.total_steps_executed_j1,
            total_steps_executed_j2=bundle.total_steps_executed_j2,
            total_steps_executed_z=bundle.total_steps_executed_z,
            total_steps_executed_j4=bundle.total_steps_executed_j4,
            following_error_j1=bundle.following_error_j1,
            following_error_j2=bundle.following_error_j2,
            following_error_z=bundle.following_error_z,
            following_error_j4=bundle.following_error_j4,
            stall_guard_flags=bundle.stall_guard_flags,
            driver_fault_flags=bundle.driver_fault_flags,
            uptime_ms=bundle.uptime_ms,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
