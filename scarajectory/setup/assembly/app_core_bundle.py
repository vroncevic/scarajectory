# -*- coding: UTF-8 -*-

'''
Module
    app_core_bundle.py
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

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scaralang.core.service.kinematics.ikinematics_service import IKinematicsService
from scaralang.core.service.trajectory.validation. \
    itrajectory_validator import (
        ITrajectoryValidator,
    )

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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
                | kinematics - IKinematicsService forward and inverse.
                | validator - ITrajectoryValidator trajectory checker.
    '''

    bounds: ScaraBounds
    transmission: TransmissionParameters
    kinematics: IKinematicsService
    validator: ITrajectoryValidator
