# -*- coding: UTF-8 -*-

'''
Module
    counts_test.py
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
    Unit tests for ProgressCounts immutable telemetry model.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from unittest import TestCase, main

from scarajectory.core.model.telemetry.counts import ProgressCounts

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ProgressCountsTestCase(TestCase):
    '''
        Tests for ProgressCounts telemetry model.

        It defines:

            :methods:
                | test_counts_creation - Verifies attribute assignment during initialization.
                | test_counts_immutability - Verifies frozen instance constraints.
                | test_equality - Verifies value equality across instances.
    '''

    def test_counts_creation(self) -> None:
        '''
            Verifies attribute values set during initialization.

            :exceptions: None.
        '''
        counts = ProgressCounts(
            total=100,
            sent=50,
            completed=48,
            failed=2,
        )
        self.assertEqual(counts.total, 100)
        self.assertEqual(counts.sent, 50)
        self.assertEqual(counts.completed, 48)
        self.assertEqual(counts.failed, 2)

    def test_counts_immutability(self) -> None:
        '''
            Verifies that modifying attributes on frozen ProgressCounts raises FrozenInstanceError.

            :exceptions: None.
        '''
        counts = ProgressCounts(
            total=0,
            sent=0,
            completed=0,
            failed=0,
        )
        with self.assertRaises(FrozenInstanceError):
            setattr(counts, 'total', 10)

    def test_equality(self) -> None:
        '''
            Verifies value equality across identical ProgressCounts instances.

            :exceptions: None.
        '''
        c1 = ProgressCounts(
            total=10,
            sent=5,
            completed=5,
            failed=0,
        )
        c2 = ProgressCounts(
            total=10,
            sent=5,
            completed=5,
            failed=0,
        )
        self.assertEqual(c1, c2)


if __name__ == '__main__':
    main()
