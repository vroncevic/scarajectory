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
    Unit tests for ScaralangFactory root subsystem factory.
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
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter
from scarajectory.infrastructure.scaralang.dependencies import ScaralangDependencies
from scarajectory.infrastructure.scaralang.factory import ScaralangFactory
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangFactoryTest(TestCase):
    '''Test suite verifying ScaralangFactory subsystem assembly.'''

    def test_create(self) -> None:
        '''Verifies create wires avoidance and shape subsystems into ScaralangProvides.'''
        bounds: ScaraBounds = ScaraBounds(
            links=LinkDimensions(l1=230.0, l2=180.0),
            vertical=VerticalBounds(z_min=-10.0, z_max=160.0),
            speeds=SpeedLimits(
                min_speed=4.0,
                max_speed=260.0,
                default_speed=55.0,
                default_accel=110.0,
                max_accel=520.0,
            ),
            joints=JointAngleBounds(
                j1_min_rad=-1.60,
                j1_max_rad=1.60,
                j2_min_rad=-2.70,
                j2_max_rad=2.70,
            ),
            singularity=SingularityMargins(
                singularity_outer_margin_mm=12.0,
                singularity_inner_margin_mm=6.0,
                singularity_theta2_min_rad=0.06,
                deadzone_r_min=48.0,
            ),
        )

        deps: ScaralangDependencies = ScaralangDependencies(bounds=bounds)
        provides: ScaralangProvides = ScaralangFactory.create(dependencies=deps)

        self.assertIsInstance(provides, ScaralangProvides)
        self.assertIsInstance(
            provides.dead_zone_avoidance, IDeadZoneAvoidanceAdapter
        )
        self.assertIsInstance(provides.shape_planner, IShapePlannerAdapter)
        self.assertIsInstance(provides.boundary, IWorkspaceBoundaryAdapter)


    def test_get_version(self) -> None:
        '''Verifies get_version returns factory version string.'''
        self.assertEqual(ScaralangFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
