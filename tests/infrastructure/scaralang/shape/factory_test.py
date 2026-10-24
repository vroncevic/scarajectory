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
    Unit tests for ShapePlannerAdapterFactory.
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
from scarajectory.infrastructure.scaralang.shape.factory import ShapePlannerAdapterFactory
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapePlannerAdapterFactoryTest(TestCase):
    '''Test suite verifying ShapePlannerAdapterFactory construction methods.'''

    def test_create(self) -> None:
        '''Verifies create configures an IShapePlannerAdapter instance from bounds.'''
        bounds: ScaraBounds = ScaraBounds(
            links=LinkDimensions(l1=210.0, l2=190.0),
            vertical=VerticalBounds(z_min=-5.0, z_max=140.0),
            speeds=SpeedLimits(
                min_speed=6.0,
                max_speed=240.0,
                default_speed=45.0,
                default_accel=95.0,
                max_accel=480.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-1.50,
                j1_max_rad=1.50,
                j2_min_rad=-2.55,
                j2_max_rad=2.55,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=9.0,
                singularity_inner_margin_mm=4.5,
                singularity_theta2_min_rad=0.04,
                deadzone_r_min=52.0,
            ),
        )

        adapter: IShapePlannerAdapter = ShapePlannerAdapterFactory.create(
            bounds=bounds,
        )
        self.assertIsInstance(adapter, IShapePlannerAdapter)

    def test_get_version(self) -> None:
        '''Verifies get_version returns factory version string.'''
        self.assertEqual(ShapePlannerAdapterFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
