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
    Subsystem factory instantiating and assembling all scaralang adapters.
'''

from __future__ import annotations

from scarajectory.infrastructure.scaralang.avoidance.factory import DeadZoneAvoidanceAdapterFactory
from scarajectory.infrastructure.scaralang.boundary.factory import WorkspaceBoundaryAdapterFactory
from scarajectory.infrastructure.scaralang.dependencies import ScaralangDependencies
from scarajectory.infrastructure.scaralang.provides import ScaralangProvides
from scarajectory.infrastructure.scaralang.shape.factory import ShapePlannerAdapterFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ScaralangFactory:
    '''
        Factory providing all scaralang infrastructure adapters bundled into ScaralangProvides.

        It defines:

            :methods:
                | create - Builds and bundles all scaralang adapters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ScaralangDependencies) -> ScaralangProvides:
        '''
            Builds and bundles all scaralang adapters using supplied dependencies.

            :param dependencies: ScaralangDependencies containing manipulator bounds.
            :return: Immutable ScaralangProvides container.
            :exceptions: None.
        '''
        return ScaralangProvides(
            dead_zone_avoidance=DeadZoneAvoidanceAdapterFactory.create(
                bounds=dependencies.bounds
            ),
            shape_planner=ShapePlannerAdapterFactory.create(
                bounds=dependencies.bounds
            ),
            boundary=WorkspaceBoundaryAdapterFactory.create(),
        )


    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
