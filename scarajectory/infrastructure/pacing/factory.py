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
    Factory service constructing PacingProvides subsystem components.
'''

from __future__ import annotations

from scarajectory.infrastructure.pacing.controller.dependencies import ControllerDependencies
from scarajectory.infrastructure.pacing.controller.factory import ControllerFactory
from scarajectory.infrastructure.pacing.controller.provides import ControllerProvides
from scarajectory.infrastructure.pacing.coordinator.dependencies import CoordinatorDependencies
from scarajectory.infrastructure.pacing.coordinator.factory import CoordinatorFactory
from scarajectory.infrastructure.pacing.coordinator.provides import CoordinatorProvides
from scarajectory.infrastructure.pacing.dependencies import PacingDependencies
from scarajectory.infrastructure.pacing.provides import PacingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PacingFactory:
    '''
        Factory providing creation of PacingProvides subsystem components.

        It defines:

            :methods:
                | create - Constructs and returns a PacingProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: PacingDependencies) -> PacingProvides:
        '''
            Constructs and returns PacingProvides instance with wired sub-factories.

            :param dependencies: Injected PacingDependencies bundle.
            :return: PacingProvides instance.
            :exceptions: None.
        '''
        coord_provides: CoordinatorProvides = CoordinatorFactory.create(
            CoordinatorDependencies(flow_barrier=dependencies.flow_barrier)
        )
        ctrl_provides: ControllerProvides = ControllerFactory.create(
            ControllerDependencies(
                flow_barrier_coordinator=coord_provides.flow_barrier_coordinator,
                capacity=dependencies.capacity,
            )
        )

        return PacingProvides(
            flow_pacing_controller=ctrl_provides.flow_pacing_controller,
            flow_barrier_coordinator=coord_provides.flow_barrier_coordinator,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
