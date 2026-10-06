# -*- coding: UTF-8 -*-

'''
Module
    iplan_command_service_test.py
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
    Unit testing for IPlanCommandService protocol specification.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.service.trajectory.contract.iplan_command_service import IPlanCommandService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanCommandServiceStub:
    '''Structural test stub satisfying IPlanCommandService protocol.'''

    def clear_plan(self) -> None:
        '''Clears all waypoints.'''

    def undo(self) -> bool:
        '''Reverts last change.'''
        return True

    def redo(self) -> bool:
        '''Re-applies change.'''
        return False

    def new_plan(self) -> None:
        '''Resets active plan.'''


class IncompletePlanCommandStub:
    '''Incomplete test stub missing required methods.'''

    def clear_plan(self) -> None:
        '''Clears all waypoints.'''

    def undo(self) -> bool:
        '''Reverts last change.'''
        return True


class PlanCommandServiceTestCase(TestCase):
    '''Unit tests validating structural protocol runtime checks for IPlanCommandService.'''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IPlanCommandService protocol.'''
        stub = PlanCommandServiceStub()
        self.assertIsInstance(stub, IPlanCommandService)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies incomplete class fails IPlanCommandService protocol check.'''
        incomplete = IncompletePlanCommandStub()
        self.assertNotIsInstance(incomplete, IPlanCommandService)


if __name__ == '__main__':
    main()
