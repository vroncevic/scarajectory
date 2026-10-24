# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Immutable value bundle holding assembled core kinematics and validation.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters
from scaralang.core.service.kinematics.provides import KinematicsProvides

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.scaralang.avoidance.iadapter import IDeadZoneAvoidanceAdapter
from scarajectory.infrastructure.scaralang.boundary.iadapter import IWorkspaceBoundaryAdapter
from scarajectory.infrastructure.scaralang.shape.iadapter import IShapePlannerAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class AppCoreBundle:
    '''
        Bundle containing assembled domain core services and parameters.

        It defines:

            :attributes:
                | bounds - ScaraBounds workspace bounds model.
                | transmission - TransmissionParameters mechanism model.
                | kinematics - KinematicsProvides kinematics subsystem provides.
                | validator - ITrajectoryValidator trajectory checker.
                | avoidance_adapter - IDeadZoneAvoidanceAdapter dead zone bypass port.
                | planner_adapter - IShapePlannerAdapter contour and circle avoidance planner port.
                | boundary_adapter - IWorkspaceBoundaryAdapter workspace boundary visualization port.
    '''

    bounds: ScaraBounds
    transmission: TransmissionParameters
    kinematics: KinematicsProvides
    validator: ITrajectoryValidator
    avoidance_adapter: IDeadZoneAvoidanceAdapter
    planner_adapter: IShapePlannerAdapter
    boundary_adapter: IWorkspaceBoundaryAdapter
