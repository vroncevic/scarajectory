# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_snapshot_factory_test.py
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
    Unit tests for DiagnosticsSnapshotFactory telemetry snapshot factory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics_bundle import DiagnosticsBundle
from scarajectory.core.model.telemetry.diagnostics_snapshot import DiagnosticsSnapshot
from scarajectory.core.service.telemetry.diagnostics_snapshot_factory import (
    DiagnosticsSnapshotFactory,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsSnapshotFactoryTestCase(TestCase):
    '''
        Tests for DiagnosticsSnapshotFactory component.

        It defines:

            :methods:
                | test_create_snapshot - Verifies snapshot model creation from diagnostics bundle.
                | test_get_version - Verifies factory version accessor string.
    '''

    def test_create_snapshot(self) -> None:
        '''
            Verifies snapshot model creation from diagnostics bundle.

            :exceptions: None.
        '''
        bundle = DiagnosticsBundle(
            rx_frames_total=100,
            tx_frames_total=80,
            crc_errors=1,
            rx_buffer_overruns=0,
            queue_high_watermark=14,
            mem_pool_min_free=128,
            total_steps_executed_j1=1000,
            total_steps_executed_j2=2000,
            total_steps_executed_z=500,
            total_steps_executed_j4=0,
            following_error_j1=2,
            following_error_j2=1,
            following_error_z=0,
            following_error_j4=0,
            stall_guard_flags=0,
            driver_fault_flags=0,
            uptime_ms=60000,
        )
        snapshot = DiagnosticsSnapshotFactory.create(bundle=bundle)
        self.assertIsInstance(snapshot, DiagnosticsSnapshot)
        self.assertEqual(snapshot.rx_frames_total, 100)
        self.assertEqual(snapshot.tx_frames_total, 80)
        self.assertEqual(snapshot.crc_errors, 1)
        self.assertEqual(snapshot.queue_high_watermark, 14)
        self.assertEqual(snapshot.uptime_ms, 60000)

    def test_get_version(self) -> None:
        '''
            Verifies factory version accessor string.

            :exceptions: None.
        '''
        self.assertEqual(DiagnosticsSnapshotFactory.get_version(), '1.0.4')


if __name__ == '__main__':
    main()
