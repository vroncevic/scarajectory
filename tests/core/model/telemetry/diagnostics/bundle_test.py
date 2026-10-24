# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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

from scarajectory.core.model.telemetry.diagnostics.bundle import DiagnosticsBundle
from scarajectory.core.model.telemetry.diagnostics.comm import CommunicationsDiagnostics
from scarajectory.core.model.telemetry.diagnostics.driver import DriverFaultDiagnostics
from scarajectory.core.model.telemetry.diagnostics.errors import FollowingErrorsDiagnostics
from scarajectory.core.model.telemetry.diagnostics.steps import JointStepsDiagnostics

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
        comm = CommunicationsDiagnostics(
            rx_frames_total=100,
            tx_frames_total=95,
            crc_errors=2,
            rx_buffer_overruns=0,
            queue_high_watermark=16,
            mem_pool_min_free=128,
            uptime_ms=60000,
        )
        steps = JointStepsDiagnostics(
            j1=5000,
            j2=4000,
            z=1000,
            j4=500,
        )
        errors = FollowingErrorsDiagnostics(
            j1=3,
            j2=1,
            z=0,
            j4=0,
        )
        driver = DriverFaultDiagnostics(
            stall_guard_flags=0,
            driver_fault_flags=0,
        )
        bundle = DiagnosticsBundle(
            comm=comm,
            steps=steps,
            following_errors=errors,
            driver=driver,
        )
        self.assertEqual(bundle.comm, comm)
        self.assertEqual(bundle.steps, steps)
        self.assertEqual(bundle.following_errors, errors)
        self.assertEqual(bundle.driver, driver)

    def test_bundle_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen DiagnosticsBundle raises FrozenInstanceError.

            :exceptions: None.
        '''
        comm = CommunicationsDiagnostics(
            rx_frames_total=0,
            tx_frames_total=0,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=0,
            mem_pool_min_free=0,
            uptime_ms=0,
        )
        steps = JointStepsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        errors = FollowingErrorsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        driver = DriverFaultDiagnostics(
            stall_guard_flags=0,
            driver_fault_flags=0,
        )
        bundle = DiagnosticsBundle(
            comm=comm,
            steps=steps,
            following_errors=errors,
            driver=driver,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(bundle, 'comm', comm)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical DiagnosticsBundle instances.

            :exceptions: None.
        '''
        comm = CommunicationsDiagnostics(
            rx_frames_total=10,
            tx_frames_total=10,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=5,
            mem_pool_min_free=50,
            uptime_ms=1000,
        )
        steps = JointStepsDiagnostics(
            j1=100,
            j2=200,
            z=300,
            j4=400,
        )
        errors = FollowingErrorsDiagnostics(
            j1=0,
            j2=0,
            z=0,
            j4=0,
        )
        driver = DriverFaultDiagnostics(
            stall_guard_flags=0,
            driver_fault_flags=0,
        )
        b1 = DiagnosticsBundle(
            comm=comm,
            steps=steps,
            following_errors=errors,
            driver=driver,
        )
        b2 = DiagnosticsBundle(
            comm=comm,
            steps=steps,
            following_errors=errors,
            driver=driver,
        )
        self.assertEqual(b1, b2)


if __name__ == '__main__':
    main()
