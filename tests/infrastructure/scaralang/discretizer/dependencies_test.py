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
    Unit tests for DiscretizerDependencies parameter bundle.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.compiler.binary.step.duration.icalculator import ISegmentDurationCalculator
from scaralang.core.service.kinematics.solver.analytical.spatial.isolver import ISpatialKinematicsSolver
from scaralang.core.service.kinematics.solver.numerical.spatial.isolver import INumericalSpatialKinematicsSolver
from scaralang.core.service.kinematics.transmission.iconverter import IJointStepTransmissionConverter

from scarajectory.infrastructure.scaralang.discretizer.dependencies import DiscretizerDependencies

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DiscretizerDependenciesTestCase(TestCase):
    '''
        Unit tests for DiscretizerDependencies.

        It defines:

            :methods:
                | test_initialization - Verifies attributes storage in parameter bundle.
    '''

    def test_initialization(self) -> None:
        '''
            Verifies attributes storage in parameter bundle.

            :exceptions: None.
        '''
        mock_spatial = MagicMock(spec=ISpatialKinematicsSolver)
        mock_numerical = MagicMock(spec=INumericalSpatialKinematicsSolver)
        mock_transmission = MagicMock(spec=IJointStepTransmissionConverter)
        mock_duration = MagicMock(spec=ISegmentDurationCalculator)
        mock_bounds = MagicMock(spec=ScaraBounds)

        deps = DiscretizerDependencies(
            spatial=mock_spatial,
            numerical_spatial=mock_numerical,
            transmission=mock_transmission,
            duration_calculator=mock_duration,
            bounds=mock_bounds,
        )
        self.assertIs(deps.spatial, mock_spatial)
        self.assertIs(deps.numerical_spatial, mock_numerical)
        self.assertIs(deps.transmission, mock_transmission)
        self.assertIs(deps.duration_calculator, mock_duration)
        self.assertIs(deps.bounds, mock_bounds)


if __name__ == '__main__':
    main()
