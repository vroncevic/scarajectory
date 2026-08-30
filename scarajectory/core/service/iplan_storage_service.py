# -*- coding: UTF-8 -*-

'''
Module
    iplan_storage_service.py
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
    Defines interface IPlanStorageService for trajectory persistence.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.itrajectory_plan import ITrajectoryPlan

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IPlanStorageService(Protocol):
    '''
        Protocol for storing and loading trajectory plan files.

        It defines:

            :methods:
                | save_plan - Saves current trajectory plan to file path.
                | load_plan - Loads waypoints from file path.
    '''

    def save_plan(self, plan: ITrajectoryPlan, filepath: str) -> None:
        '''
            Saves current trajectory plan to file path.

            :param plan: ITrajectoryPlan instance to save.
            :param filepath: Target JSON file path.
            :exceptions: OSError.
        '''

    def load_plan(self, filepath: str) -> list[Waypoint]:
        '''
            Loads waypoints from file path.

            :param filepath: Source JSON file path.
            :return: List of loaded Waypoint entities.
            :exceptions: OSError.
        '''
