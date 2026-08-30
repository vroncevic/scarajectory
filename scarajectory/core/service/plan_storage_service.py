# -*- coding: UTF-8 -*-

'''
Module
    plan_storage_service.py
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
    Dedicated service implementation for trajectory plan serialization and file persistence.
'''

from __future__ import annotations

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.model.trajectory_serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class PlanStorageService:
    '''
        Service handling JSON trajectory persistence and file I/O operations.

        It defines:

            :methods:
                | save_plan - Saves trajectory plan waypoints to JSON file path.
                | load_plan - Loads and deserializes waypoints from JSON file path.
    '''

    def save_plan(self, plan: ITrajectoryPlan, filepath: str) -> None:
        '''
            Saves trajectory plan waypoints to JSON file path.

            :param plan: ITrajectoryPlan instance.
            :param filepath: Target file path.
            :exceptions: OSError.
        '''
        TrajectorySerializer.save_json(plan.waypoints, filepath)

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads and deserializes waypoints from JSON file path.

            :param filepath: Source file path.
            :return: List of loaded Waypoint instances.
            :exceptions: OSError.
        '''
        return TrajectorySerializer.load_json(filepath)
