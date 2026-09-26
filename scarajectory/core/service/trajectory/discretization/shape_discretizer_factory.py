'''
Module
    shape_discretizer_factory.py
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
    Factory instantiating ShapeDiscretizer with domain WaypointFactory.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.discretization.iwaypoint_factory import IWaypointFactory
from scarajectory.core.service.trajectory.discretization.shape_discretizer import ShapeDiscretizer
from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ShapeDiscretizerFactory:
    '''
        Factory providing creation of ShapeDiscretizer service instances.

        It defines:

            :methods:
                | create - Builds ShapeDiscretizer with default domain WaypointFactory.
                | create_with_waypoint_factory - Builds ShapeDiscretizer with injected IWaypointFactory.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls) -> ShapeDiscretizer:
        '''
            Builds and returns a ShapeDiscretizer instance with internal WaypointFactory.

            :return: ShapeDiscretizer instance.
            :exceptions: None.
        '''
        return ShapeDiscretizer(waypoint_factory=WaypointFactory())

    @classmethod
    def create_with_waypoint_factory(
        cls,
        *,
        waypoint_factory: IWaypointFactory,
    ) -> ShapeDiscretizer:
        '''
            Builds and returns a ShapeDiscretizer instance with injected IWaypointFactory.

            :param waypoint_factory: Injected IWaypointFactory instance.
            :return: ShapeDiscretizer instance.
            :exceptions: None.
        '''
        return ShapeDiscretizer(waypoint_factory=waypoint_factory)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__

