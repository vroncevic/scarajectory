# -*- coding: UTF-8 -*-

'''
Module
    iplan_persistence_service_test.py
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
    Unit testing for IPlanPersistenceService protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.contract.iplan_persistence_service import (
    IPlanPersistenceService,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanPersistenceServiceStub:
    '''Structural test stub satisfying IPlanPersistenceService protocol.'''

    def save_plan(self, filepath: str) -> None:
        '''Saves current plan.'''

    def load_plan(self, filepath: str) -> None:
        '''Loads plan from path.'''


class IncompletePlanPersistenceStub:
    '''Incomplete test stub missing required load_plan method.'''

    def save_plan(self, filepath: str) -> None:
        '''Saves current plan.'''

    def clear_cache(self) -> None:
        '''Non-protocol method maintaining minimum method count.'''


class PlanPersistenceServiceTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IPlanPersistenceService.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IPlanPersistenceService protocol.'''
        stub = PlanPersistenceServiceStub()
        self.assertIsInstance(stub, IPlanPersistenceService)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IPlanPersistenceService protocol check.'''
        incomplete = IncompletePlanPersistenceStub()
        self.assertNotIsInstance(incomplete, IPlanPersistenceService)


if __name__ == '__main__':
    main()
