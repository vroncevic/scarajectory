# -*- coding: UTF-8 -*-

'''
Module
    communication_events_test.py
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
    Unit tests for MoveEvent, FaultEvent, DiagnosticsSnapshot and their factories.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.event.move_event import MoveEvent
from scarajectory.core.model.communication.event.fault_event import FaultEvent
from scarajectory.core.model.communication.telemetry.diagnostics_bundle import DiagnosticsBundle
from scarajectory.core.model.communication.telemetry.diagnostics_snapshot import DiagnosticsSnapshot
from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.communication.event.move_event_factory import MoveEventFactory
from scarajectory.core.service.communication.event.fault_event_factory import FaultEventFactory
from scarajectory.core.service.communication.telemetry.diagnostics_snapshot_factory import DiagnosticsSnapshotFactory


__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestCommunicationEvents(TestCase):
    '''
        Test suite for communication event models and factory services.
    '''

    def test_move_event_factory(self) -> None:
        self.assertTrue(issubclass(MoveEventFactory, object))
        evt: MoveEvent = MoveEventFactory.create(event_type=2, segment_id=42)
        self.assertIsInstance(evt, MoveEvent)
        self.assertEqual(evt.event_type, 2)
        self.assertEqual(evt.segment_id, 42)

    def test_fault_event_factory(self) -> None:
        self.assertTrue(issubclass(FaultEventFactory, object))
        evt: FaultEvent = FaultEventFactory.create(severity=2, fault_code=5, extra_info=100)
        self.assertIsInstance(evt, FaultEvent)
        self.assertEqual(evt.severity, 2)
        self.assertEqual(evt.fault_code, 5)
        self.assertEqual(evt.extra_info, 100)

    def test_diagnostics_snapshot_factory(self) -> None:
        self.assertTrue(issubclass(DiagnosticsSnapshotFactory, object))
        bundle = DiagnosticsBundle(
            rx_frames_total=10,
            tx_frames_total=12,
            crc_errors=0,
            rx_buffer_overruns=0,
            queue_high_watermark=3,
            mem_pool_min_free=15,
            total_steps_executed_j1=1000,
            total_steps_executed_j2=1500,
            total_steps_executed_z=200,
            total_steps_executed_j4=0,
            following_error_j1=1,
            following_error_j2=-1,
            following_error_z=0,
            following_error_j4=0,
            stall_guard_flags=0,
            driver_fault_flags=0,
            uptime_ms=3600000,
        )
        self.assertIsInstance(bundle, DiagnosticsBundle)
        diag: DiagnosticsSnapshot = DiagnosticsSnapshotFactory.create(bundle=bundle)
        self.assertIsInstance(diag, DiagnosticsSnapshot)
        self.assertEqual(diag.uptime_ms, 3600000)
        self.assertEqual(diag.queue_high_watermark, 3)

    def test_protocol_mode_enum(self) -> None:
        self.assertEqual(ProtocolMode.ASCII.value, 'ascii')
        self.assertEqual(ProtocolMode.BINARY.value, 'binary')


if __name__ == '__main__':
    main()
