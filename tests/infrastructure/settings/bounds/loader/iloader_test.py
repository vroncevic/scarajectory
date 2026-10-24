# -*- coding: UTF-8 -*-

'''
Module
    iloader_test.py
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
    Unit testing for IScaraBoundsLoader protocol conformance.
'''

from __future__ import annotations

from collections.abc import Mapping
from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.angle import JointAngleBounds
from scaralang.core.model.kinematics.profile.link import LinkDimensions
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.singularity import SingularityMargins
from scaralang.core.model.kinematics.profile.speed import SpeedLimits
from scaralang.core.model.kinematics.profile.vertical import VerticalBounds

from scarajectory.infrastructure.settings.bounds.loader.iloader import IScaraBoundsLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


def create_sample_bounds() -> ScaraBounds:
    '''
        Creates a sample ScaraBounds instance for testing.

        :return: Initialized ScaraBounds.
        :exceptions: None.
    '''
    return ScaraBounds(
        links=LinkDimensions(l1=150.0, l2=120.0),
        vertical=VerticalBounds(z_min=0.0, z_max=100.0),
        speeds=SpeedLimits(
            min_speed=1.0,
            max_speed=250.0,
            default_speed=50.0,
            default_accel=300.0,
            max_accel=2000.0,
        ),
        joints=JointAngleBounds(
            j1_min_rad=-2.6,
            j1_max_rad=2.6,
            j2_min_rad=-2.5,
            j2_max_rad=2.5,
        ),
        singularity=SingularityMargins(
            singularity_outer_margin_mm=3.0,
            singularity_inner_margin_mm=3.0,
            singularity_theta2_min_rad=0.08,
            deadzone_r_min=86.0,
        ),
    )


class ConformingBoundsLoaderStub:
    '''Conforming stub implementation satisfying IScaraBoundsLoader protocol.'''

    def load_bounds(self) -> ScaraBounds:
        '''Loads bounds.'''
        return create_sample_bounds()

    def load_bounds_with_options(
        self, *, options: Mapping[str, object]
    ) -> ScaraBounds:
        '''Loads bounds with options.'''
        _ = options
        return create_sample_bounds()


class IncompleteBoundsLoaderStub:
    '''Non-conforming stub implementation missing load_bounds_with_options.'''

    def load_bounds(self) -> ScaraBounds:
        '''Loads bounds.'''
        return create_sample_bounds()

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class ScaraBoundsLoaderProtocolTestCase(TestCase):
    '''
        Tests IScaraBoundsLoader runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies IScaraBoundsLoader protocol.'''
        stub = ConformingBoundsLoaderStub()
        self.assertIsInstance(stub, IScaraBoundsLoader)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails IScaraBoundsLoader protocol check.'''
        stub = IncompleteBoundsLoaderStub()
        self.assertNotIsInstance(stub, IScaraBoundsLoader)


if __name__ == '__main__':
    main()
