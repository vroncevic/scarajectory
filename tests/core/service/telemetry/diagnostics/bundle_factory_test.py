# -*- coding: UTF-8 -*-

'''
Module
    bundle_factory_test.py
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
    Unit tests for DiagnosticsBundleFactory domain factory service.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.bundle import DiagnosticsBundle
from scarajectory.core.model.telemetry.diagnostics.comm import CommunicationsDiagnostics
from scarajectory.core.model.telemetry.diagnostics.driver import DriverFaultDiagnostics
from scarajectory.core.model.telemetry.diagnostics.errors import FollowingErrorsDiagnostics
from scarajectory.core.model.telemetry.diagnostics.steps import JointStepsDiagnostics
from scarajectory.core.service.telemetry.diagnostics.bundle_factory import DiagnosticsBundleFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiagnosticsBundleFactoryTestCase(TestCase):
    '''
        Tests for DiagnosticsBundleFactory component.

        It defines:

            :methods:
                | test_create_diagnostics_bundle - Verifies diagnostics bundle creation.
                | test_get_version - Verifies factory version accessor string.
    '''

    def test_create_diagnostics_bundle(self) -> None:
        '''
            Verifies diagnostics bundle creation.

            :exceptions: None.
        '''
        comm = CommunicationsDiagnostics(
            rx_frames_total=100,
            tx_frames_total=95,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=10,
            mem_pool_min_free=512,
            uptime_ms=12000,
        )
        steps = JointStepsDiagnostics(j1=1000, j2=2000, z=500, j4=100)
        errors = FollowingErrorsDiagnostics(j1=2, j2=1, z=0, j4=0)
        driver = DriverFaultDiagnostics(stall_guard_flags=0, driver_fault_flags=0)
        bundle = DiagnosticsBundleFactory.create(
            comm=comm,
            steps=steps,
            following_errors=errors,
            driver=driver,
        )
        self.assertIsInstance(bundle, DiagnosticsBundle)
        self.assertEqual(bundle.comm, comm)
        self.assertEqual(bundle.steps, steps)
        self.assertEqual(bundle.following_errors, errors)
        self.assertEqual(bundle.driver, driver)

    def test_get_version(self) -> None:
        '''
            Verifies factory version accessor string.

            :exceptions: None.
        '''
        self.assertEqual(DiagnosticsBundleFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
