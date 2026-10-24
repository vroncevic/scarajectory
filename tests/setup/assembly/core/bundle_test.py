# -*- coding: UTF-8 -*-

'''
Module
    bundle_test.py
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
    Unit tests for AppCoreBundle value object.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.service.kinematics.provides import KinematicsProvides

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter
from scarajectory.setup.assembly.core.bundle import AppCoreBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppCoreBundleTest(TestCase):
    '''
        Test suite verifying AppCoreBundle structure.

        It defines:

            :methods:
                | test_bundle_creation - Tests creating bundle with mock components.
    '''

    def test_bundle_creation(self) -> None:
        '''
            Verifies AppCoreBundle stores and exposes attributes.

            :exceptions: None.
        '''
        bounds: MagicMock = MagicMock(spec=ScaraBounds)
        trans: MagicMock = MagicMock(spec=TransmissionParameters)
        kin: MagicMock = MagicMock(spec=KinematicsProvides)
        val: MagicMock = MagicMock(spec=ITrajectoryValidator)
        avoid: MagicMock = MagicMock(spec=IDeadZoneAvoidanceAdapter)
        planner: MagicMock = MagicMock(spec=IShapePlannerAdapter)
        boundary: MagicMock = MagicMock(spec=IWorkspaceBoundaryAdapter)

        bundle: AppCoreBundle = AppCoreBundle(
            bounds=bounds,
            transmission=trans,
            kinematics=kin,
            validator=val,
            avoidance_adapter=avoid,
            planner_adapter=planner,
            boundary_adapter=boundary,
        )
        self.assertIs(bundle.bounds, bounds)
        self.assertIs(bundle.transmission, trans)
        self.assertIs(bundle.kinematics, kin)
        self.assertIs(bundle.validator, val)
        self.assertIs(bundle.avoidance_adapter, avoid)
        self.assertIs(bundle.planner_adapter, planner)
        self.assertIs(bundle.boundary_adapter, boundary)


if __name__ == '__main__':
    main()
