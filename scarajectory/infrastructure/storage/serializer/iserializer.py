# -*- coding: UTF-8 -*-

'''
Module
    iserializer.py
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
    Defines structural protocol ITrajectorySerializer for waypoint and plan serialization.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectorySerializer(Protocol):
    '''
        Structural protocol for serializing and deserializing waypoints and trajectories.

        It defines:

            :methods:
                | serialize_waypoint - Converts a single TrajectoryWaypoint into a dictionary.
                | deserialize_waypoint - Reconstructs a single TrajectoryWaypoint from dictionary data.
                | serialize_to_dict - Converts waypoints sequence into a versioned dictionary.
                | deserialize_from_dict - Reconstructs waypoints list from dictionary data.
                | serialize_to_json - Encodes waypoints sequence into formatted JSON string.
                | deserialize_from_json - Decodes JSON string into a list of waypoints.
    '''

    def serialize_waypoint(
        self,
        waypoint: TrajectoryWaypoint
    ) -> dict[str, float | str]:
        '''
            Serializes a single TrajectoryWaypoint to dictionary format.

            :param waypoint: TrajectoryWaypoint instance to serialize.
            :return: Dictionary containing waypoint fields.
        '''

    def deserialize_waypoint(
        self,
        data: dict[str, object]
    ) -> TrajectoryWaypoint:
        '''
            Deserializes a single TrajectoryWaypoint from dictionary data.

            :param data: Dictionary containing waypoint fields.
            :return: Reconstructed TrajectoryWaypoint instance.
        '''

    def serialize_to_dict(
        self,
        waypoints: Sequence[TrajectoryWaypoint]
    ) -> dict[str, object]:
        '''
            Converts sequence of waypoints into a versioned dictionary structure.

            :param waypoints: Sequence of TrajectoryWaypoint instances.
            :return: Dictionary containing schema version and waypoints payload.
        '''

    def deserialize_from_dict(
        self,
        data: dict[str, object]
    ) -> list[TrajectoryWaypoint]:
        '''
            Reconstructs list of Waypoints from dictionary data.

            :param data: Dictionary containing waypoints list.
            :return: List of restored TrajectoryWaypoint instances.
        '''

    def serialize_to_json(
        self,
        waypoints: Sequence[TrajectoryWaypoint]
    ) -> str:
        '''
            Encodes waypoints sequence into formatted JSON string.

            :param waypoints: Sequence of TrajectoryWaypoint instances.
            :return: Formatted JSON string representation.
        '''

    def deserialize_from_json(
        self,
        json_str: str
    ) -> list[TrajectoryWaypoint]:
        '''
            Decodes JSON string into a list of waypoints.

            :param json_str: JSON string containing serialized waypoints.
            :return: List of restored TrajectoryWaypoint instances.
        '''
