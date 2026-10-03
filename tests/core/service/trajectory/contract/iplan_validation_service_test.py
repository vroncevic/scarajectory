# -*- coding: UTF-8 -*-

'''
Module
    iplan_validation_service_test.py
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
    Unit testing for IPlanValidationService protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.contract.iplan_validation_service import (
    IPlanValidationService,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanValidationServiceStub:
    '''Structural test stub satisfying IPlanValidationService protocol.'''

    def validate_plan(self) -> tuple[bool, list[str]]:
        '''Validates trajectory plan.'''
        return (True, ['All kinematic limits satisfied'])

    def get_last_report(self) -> list[str]:
        '''Returns cached validation messages.'''
        return ['OK']


class IncompletePlanValidationStub:
    '''Incomplete test stub missing required validate_plan method.'''

    def get_report(self) -> list[str]:
        '''Returns report.'''
        return []

    def clear_report(self) -> None:
        '''Clears report.'''


class PlanValidationServiceTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IPlanValidationService.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IPlanValidationService protocol.'''
        stub = PlanValidationServiceStub()
        self.assertIsInstance(stub, IPlanValidationService)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IPlanValidationService protocol check.'''
        incomplete = IncompletePlanValidationStub()
        self.assertNotIsInstance(incomplete, IPlanValidationService)


if __name__ == '__main__':
    main()
