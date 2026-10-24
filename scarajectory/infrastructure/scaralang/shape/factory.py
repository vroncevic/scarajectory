# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating ShapePlannerAdapter components.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.trajectory.avoidance.shape.iplanner import IAvoidanceShapePlanner
from scaralang.core.service.trajectory.discretization.circle.icircle import ICircleDiscretizer
from scaralang.infrastructure.trajectory.avoidance.shape.dependencies import DefaultShapeDependencies
from scaralang.infrastructure.trajectory.avoidance.shape.factory import DefaultShapeFactory
from scaralang.infrastructure.trajectory.discretization.factory import DefaultDiscretizationFactory

from scarajectory.infrastructure.scaralang.shape.adapter import ShapePlannerAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapePlannerAdapterFactory:
    '''
        Factory providing creation of ShapePlannerAdapter instances.

        It defines:

            :methods:
                | create - Constructs adapter directly from robot workspace bounds.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(
        cls,
        bounds: ScaraBounds,
    ) -> IShapePlannerAdapter:
        '''
            Constructs adapter instance directly from robot workspace bounds.

            :param bounds: Injected ScaraBounds geometry configuration.
            :return: Configured IShapePlannerAdapter instance.
            :exceptions: None.
        '''
        shape_deps: DefaultShapeDependencies = DefaultShapeDependencies(
            bounds=bounds,
            safety_margin_mm=5.0,
            angular_step_rad=0.15,
        )
        avoidance_planner: IAvoidanceShapePlanner = (
            DefaultShapeFactory.create(dependencies=shape_deps).planner
        )
        discretizer: ICircleDiscretizer = (
            DefaultDiscretizationFactory.create().circle
        )

        return ShapePlannerAdapter(
            planner=avoidance_planner,
            discretizer=discretizer,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
