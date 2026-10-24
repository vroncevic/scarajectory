# -*- coding: UTF-8 -*-

'''
Module
    comm_test.py
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
    Unit tests for CommunicationsDiagnostics immutable telemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.diagnostics.comm import CommunicationsDiagnostics

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommunicationsDiagnosticsTestCase(TestCase):
    '''
        Tests for CommunicationsDiagnostics telemetry model.

        It defines:

            :methods:
                | test_comm_creation - Verifies attribute assignment during initialization.
                | test_comm_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_comm_creation(self) -> None:
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
        self.assertEqual(comm.rx_frames_total, 100)
        self.assertEqual(comm.tx_frames_total, 95)
        self.assertEqual(comm.crc_errors, 2)
        self.assertEqual(comm.rx_buffer_overruns, 0)
        self.assertEqual(comm.queue_high_watermark, 16)
        self.assertEqual(comm.mem_pool_min_free, 128)
        self.assertEqual(comm.uptime_ms, 60000)

    def test_comm_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen CommunicationsDiagnostics raises FrozenInstanceError.

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
        with self.assertRaises(FrozenInstanceError):
            setattr(comm, 'rx_frames_total', 10)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical CommunicationsDiagnostics instances.

            :exceptions: None.
        '''
        c1 = CommunicationsDiagnostics(
            rx_frames_total=10,
            tx_frames_total=10,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=5,
            mem_pool_min_free=50,
            uptime_ms=1000,
        )
        c2 = CommunicationsDiagnostics(
            rx_frames_total=10,
            tx_frames_total=10,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=5,
            mem_pool_min_free=50,
            uptime_ms=1000,
        )
        self.assertEqual(c1, c2)


if __name__ == '__main__':
    main()
