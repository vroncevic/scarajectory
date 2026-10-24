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
    Unit tests for DeadZoneAvoidanceAdapterFactory.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds
from scarajectory.infrastructure.scaralang.avoidance.factory import DeadZoneAvoidanceAdapterFactory
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneAvoidanceAdapterFactoryTest(TestCase):
    '''Test suite verifying DeadZoneAvoidanceAdapterFactory construction methods.'''

    def test_create(self) -> None:
        '''Verifies create configures an IDeadZoneAvoidanceAdapter instance from bounds.'''
        bounds: ScaraBounds = ScaraBounds(
            links=LinkDimensions(l1=225.0, l2=175.0),
            vertical=VerticalBounds(z_min=0.0, z_max=150.0),
            speeds=SpeedLimits(
                min_speed=5.0,
                max_speed=250.0,
                default_speed=50.0,
                default_accel=100.0,
                max_accel=500.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-1.57,
                j1_max_rad=1.57,
                j2_min_rad=-2.61,
                j2_max_rad=2.61,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=10.0,
                singularity_inner_margin_mm=5.0,
                singularity_theta2_min_rad=0.05,
                deadzone_r_min=50.0,
            ),
        )
        adapter: IDeadZoneAvoidanceAdapter = DeadZoneAvoidanceAdapterFactory.create(
            bounds=bounds,
        )
        self.assertIsInstance(adapter, IDeadZoneAvoidanceAdapter)

    def test_get_version(self) -> None:
        '''Verifies get_version returns factory version string.'''
        self.assertEqual(DeadZoneAvoidanceAdapterFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
