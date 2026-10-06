# -*- coding: UTF-8 -*-

'''
Module
    diagnostics_bundle_test.py
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
    Unit tests for DiagnosticsBundle immutable telemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics_bundle import DiagnosticsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsBundleTestCase(TestCase):
    '''
        Tests for DiagnosticsBundle telemetry data model.

        It defines:

            :methods:
                | test_bundle_creation - Verifies telemetry attribute values.
                | test_bundle_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        bundle = DiagnosticsBundle(
            rx_frames_total=100,
            tx_frames_total=95,
            crc_errors=2,
            rx_buffer_overruns=0,
            queue_high_watermark=16,
            mem_pool_min_free=128,
            total_steps_executed_j1=5000,
            total_steps_executed_j2=4000,
            total_steps_executed_z=1000,
            total_steps_executed_j4=500,
            following_error_j1=3,
            following_error_j2=1,
            following_error_z=0,
            following_error_j4=0,
            stall_guard_flags=0,
            driver_fault_flags=0,
            uptime_ms=60000,
        )
        self.assertEqual(bundle.rx_frames_total, 100)
        self.assertEqual(bundle.tx_frames_total, 95)
        self.assertEqual(bundle.crc_errors, 2)
        self.assertEqual(bundle.rx_buffer_overruns, 0)
        self.assertEqual(bundle.queue_high_watermark, 16)
        self.assertEqual(bundle.mem_pool_min_free, 128)
        self.assertEqual(bundle.total_steps_executed_j1, 5000)
        self.assertEqual(bundle.total_steps_executed_j2, 4000)
        self.assertEqual(bundle.total_steps_executed_z, 1000)
        self.assertEqual(bundle.total_steps_executed_j4, 500)
        self.assertEqual(bundle.following_error_j1, 3)
        self.assertEqual(bundle.following_error_j2, 1)
        self.assertEqual(bundle.following_error_z, 0)
        self.assertEqual(bundle.following_error_j4, 0)
        self.assertEqual(bundle.stall_guard_flags, 0)
        self.assertEqual(bundle.driver_fault_flags, 0)
        self.assertEqual(bundle.uptime_ms, 60000)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen DiagnosticsBundle raises FrozenInstanceError.

            :exceptions: None.
        '''
        bundle = DiagnosticsBundle(
            rx_frames_total=0,
            tx_frames_total=0,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=0,
            mem_pool_min_free=0,
            total_steps_executed_j1=0,
            total_steps_executed_j2=0,
            total_steps_executed_z=0,
            total_steps_executed_j4=0,
            following_error_j1=0,
            following_error_j2=0,
            following_error_z=0,
            following_error_j4=0,
            stall_guard_flags=0,
            driver_fault_flags=0,
            uptime_ms=0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(bundle, 'rx_frames_total', 10)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical DiagnosticsBundle instances.

            :exceptions: None.
        '''
        b1 = DiagnosticsBundle(
            rx_frames_total=10,
            tx_frames_total=10,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=5,
            mem_pool_min_free=50,
            total_steps_executed_j1=100,
            total_steps_executed_j2=200,
            total_steps_executed_z=300,
            total_steps_executed_j4=400,
            following_error_j1=0,
            following_error_j2=0,
            following_error_z=0,
            following_error_j4=0,
            stall_guard_flags=0,
            driver_fault_flags=0,
            uptime_ms=1000,
        )
        b2 = DiagnosticsBundle(
            rx_frames_total=10,
            tx_frames_total=10,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=5,
            mem_pool_min_free=50,
            total_steps_executed_j1=100,
            total_steps_executed_j2=200,
            total_steps_executed_z=300,
            total_steps_executed_j4=400,
            following_error_j1=0,
            following_error_j2=0,
            following_error_z=0,
            following_error_j4=0,
            stall_guard_flags=0,
            driver_fault_flags=0,
            uptime_ms=1000,
        )
        self.assertEqual(b1, b2)


if __name__ == '__main__':
    main()
