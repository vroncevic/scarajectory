# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_validator_test.py
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
    Unit tests for native ITrajectoryValidator structural protocol.
'''

from __future__ import annotations

from collections.abc import Sequence
from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MockValidator:
    '''Mock validator implementation verifying structural protocol compliance.'''

    @property
    def r_min(self) -> float:
        return 50.0

    @property
    def r_max(self) -> float:
        return 300.0

    def validate_point(self, point: Waypoint) -> object:
        return True

    def validate_feedrate(self, speed: float) -> object:
        return True

    def validate_plan(
        self,
        plan: ITrajectoryReadOnly,
    ) -> tuple[bool, Sequence[str]]:
        return True, ()


class IncompleteValidator:
    '''Incomplete validator missing required methods.'''

    @property
    def r_min(self) -> float:
        return 50.0


class ITrajectoryValidatorTest(TestCase):
    '''Test cases for ITrajectoryValidator structural protocol verification.'''

    def test_protocol_conformance(self) -> None:
        '''Verifies that a valid implementation conforms to ITrajectoryValidator.'''
        validator = MockValidator()
        self.assertIsInstance(validator, ITrajectoryValidator)
        self.assertEqual(validator.r_min, 50.0)
        self.assertEqual(validator.r_max, 300.0)

    def test_protocol_rejection(self) -> None:
        '''Verifies that an incomplete implementation is rejected.'''
        incomplete = IncompleteValidator()
        self.assertNotIsInstance(incomplete, ITrajectoryValidator)


if __name__ == '__main__':
    main()
