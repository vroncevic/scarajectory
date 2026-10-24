# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit testing for ValidationDependencies container.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.validation.dependencies import ValidationDependencies
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationDependenciesTestCase(TestCase):
    '''
        Unit tests for ValidationDependencies container.

        It defines:

            :methods:
                | test_initialization - Verifies container properties initialization.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies container properties initialization.

            :exceptions: None.
        '''
        mock_plan = MagicMock(spec=IWaypointQuery)
        mock_validator = MagicMock(spec=ITrajectoryValidator)
        mock_avoidance = MagicMock(spec=IDeadZoneAvoidanceAdapter)

        deps = ValidationDependencies(
            plan=mock_plan,
            validator=mock_validator,
            avoidance_adapter=mock_avoidance,
        )

        self.assertIs(deps.plan, mock_plan)
        self.assertIs(deps.validator, mock_validator)
        self.assertIs(deps.avoidance_adapter, mock_avoidance)


if __name__ == '__main__':
    main()
