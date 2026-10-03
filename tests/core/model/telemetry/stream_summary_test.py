# -*- coding: UTF-8 -*-

'''
Module
    stream_summary_test.py
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
    Unit tests for StreamSummary immutable statistics value object.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.stream_summary import StreamSummary

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamSummaryTestCase(TestCase):
    '''
        Tests for StreamSummary statistics container.

        It defines:

            :methods:
                | test_summary_creation - Verifies summary statistics attributes.
                | test_summary_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_summary_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        summary = StreamSummary(
            total_packets=100,
            sent_packets=100,
            acknowledged_packets=98,
            failed_packets=2,
            elapsed_time_s=12.5,
            is_completed=True,
        )
        self.assertEqual(summary.total_packets, 100)
        self.assertEqual(summary.sent_packets, 100)
        self.assertEqual(summary.acknowledged_packets, 98)
        self.assertEqual(summary.failed_packets, 2)
        self.assertAlmostEqual(summary.elapsed_time_s, 12.5)
        self.assertTrue(summary.is_completed)

    def test_summary_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen StreamSummary raises FrozenInstanceError.

            :exceptions: None.
        '''
        summary = StreamSummary(
            total_packets=50,
            sent_packets=50,
            acknowledged_packets=50,
            failed_packets=0,
            elapsed_time_s=5.0,
            is_completed=True,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(summary, 'is_completed', False)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical StreamSummary instances.

            :exceptions: None.
        '''
        s1 = StreamSummary(
            total_packets=10,
            sent_packets=10,
            acknowledged_packets=10,
            failed_packets=0,
            elapsed_time_s=1.0,
            is_completed=True,
        )
        s2 = StreamSummary(
            total_packets=10,
            sent_packets=10,
            acknowledged_packets=10,
            failed_packets=0,
            elapsed_time_s=1.0,
            is_completed=True,
        )
        self.assertEqual(s1, s2)


if __name__ == '__main__':
    main()
