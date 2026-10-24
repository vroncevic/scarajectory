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
    Factory instantiating DeadZoneAvoidanceAdapter components.
'''

from __future__ import annotations

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.trajectory.avoidance.bypass.planner.iplanner import IDeadZoneBypassPlanner
from scaralang.core.service.trajectory.avoidance.validation.ivalidator import IDeadZoneValidator
from scaralang.infrastructure.trajectory.avoidance.bypass.dependencies import DefaultBypassDependencies
from scaralang.infrastructure.trajectory.avoidance.bypass.factory import DefaultBypassFactory
from scaralang.infrastructure.trajectory.avoidance.validation.dependencies import DefaultValidationDependencies
from scaralang.infrastructure.trajectory.avoidance.validation.factory import DefaultValidationFactory

from scarajectory.infrastructure.scaralang.avoidance.adapter import DeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class DeadZoneAvoidanceAdapterFactory:
    '''
        Factory providing creation of DeadZoneAvoidanceAdapter instances.

        It defines:

            :methods:
                | create - Constructs adapter directly from robot workspace bounds.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(
        cls,
        bounds: ScaraBounds,
    ) -> IDeadZoneAvoidanceAdapter:
        '''
            Constructs adapter instance directly from robot workspace bounds.

            :param bounds: Injected ScaraBounds geometry configuration.
            :return: Configured IDeadZoneAvoidanceAdapter instance.
            :exceptions: None.
        '''
        validation_deps: DefaultValidationDependencies = DefaultValidationDependencies(
            bounds=bounds
        )
        dead_zone_val: IDeadZoneValidator = (
            DefaultValidationFactory.create(dependencies=validation_deps).validator
        )
        bypass_deps: DefaultBypassDependencies = DefaultBypassDependencies(
            validator=dead_zone_val,
            safety_margin_mm=5.0,
            angular_step_rad=0.15,
        )
        bypass_planner: IDeadZoneBypassPlanner = (
            DefaultBypassFactory.create(dependencies=bypass_deps).planner
        )
        return DeadZoneAvoidanceAdapter(
            validator=dead_zone_val,
            planner=bypass_planner,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
