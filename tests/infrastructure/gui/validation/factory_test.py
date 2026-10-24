# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for ValidationTabFactory component construction.
'''

from __future__ import annotations

from tkinter import Tk
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.core.service.trajectory.plan.store.query.iquery import IWaypointQuery
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.validation.dependencies import ValidationDependencies
from scarajectory.infrastructure.gui.validation.factory import ValidationTabFactory
from scarajectory.infrastructure.gui.validation.tab import ValidationTab
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ValidationTabFactoryTestCase(TestCase):
    '''
        Unit tests for ValidationTabFactory.

        It defines:

            :methods:
                | setUp - Initializes headless Tk instance before each test.
                | tearDown - Destroys Tk instance after each test.
                | test_create - Verifies ValidationTabFactory creates a valid ValidationTab.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def setUp(self) -> None:
        '''
            Initializes headless Tk instance before each test.

            :exceptions: None.
        '''
        self.root: Tk = Tk()
        self.root.withdraw()

    def tearDown(self) -> None:
        '''
            Destroys Tk instance after each test.

            :exceptions: None.
        '''
        self.root.destroy()

    def test_create(self) -> None:
        '''
            Verifies ValidationTabFactory creates a valid ValidationTab instance.

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

        tab = ValidationTabFactory.create(
            self.root,
            dependencies=deps,
        )
        self.assertIsInstance(tab, ValidationTab)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string.

            :exceptions: None.
        '''
        self.assertEqual(ValidationTabFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
