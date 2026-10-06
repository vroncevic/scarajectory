# -*- coding: UTF-8 -*-

'''
Module
    trajectory_serializer.py
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
    Infrastructure storage serializer and deserializer for trajectory waypoints and plans.
'''

from __future__ import annotations

from collections.abc import Sequence
from json import dumps, loads

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectorySerializer:
    '''
        Serializes and deserializes trajectory waypoints to and from in-memory dict and JSON strings.

        It defines:

            :methods:
                | serialize_waypoint - Converts a single Waypoint into a dictionary.
                | deserialize_waypoint - Reconstructs a single Waypoint from dictionary data.
                | serialize_to_dict - Converts waypoints sequence into a versioned dictionary.
                | deserialize_from_dict - Reconstructs waypoints list from dictionary data.
                | serialize_to_json - Encodes waypoints sequence into formatted JSON string.
                | deserialize_from_json - Decodes JSON string into a list of waypoints.
    '''

    @classmethod
    def serialize_waypoint(cls, waypoint: Waypoint) -> dict[str, float | str]:
        '''
            Serializes a single Waypoint to dictionary format.

            :param waypoint: Waypoint instance to serialize.
            :return: Dictionary containing waypoint fields.
        '''
        return {
            'x': round(waypoint.x, 3),
            'y': round(waypoint.y, 3),
            'z': round(waypoint.z, 3),
            'phi': round(waypoint.phi, 3),
            'speed': round(waypoint.speed, 2),
            'name': waypoint.name,
            'command': waypoint.command
        }

    @classmethod
    def deserialize_waypoint(cls, data: dict[str, object]) -> Waypoint:
        '''
            Deserializes a single Waypoint from dictionary data.

            :param data: Dictionary containing waypoint fields.
            :return: Reconstructed Waypoint instance.
        '''
        return Waypoint(
            x=float(data.get('x', 180.0)),
            y=float(data.get('y', 0.0)),
            z=float(data.get('z', 20.0)),
            phi=float(data.get('phi', 0.0)),
            speed=float(data.get('speed', 40.0)),
            name=str(data.get('name', '')),
            command=str(data.get('command', ''))
        )

    @classmethod
    def serialize_to_dict(
        cls,
        waypoints: Sequence[Waypoint]
    ) -> dict[str, object]:
        '''
            Converts sequence of waypoints into a versioned dictionary structure.

            :param waypoints: Sequence of Waypoint instances.
            :return: Dictionary containing schema version and waypoints payload.
        '''
        return {
            'version': '1.0.3',
            'waypoints': [cls.serialize_waypoint(pt) for pt in waypoints]
        }

    @classmethod
    def deserialize_from_dict(
        cls,
        data: dict[str, object]
    ) -> list[Waypoint]:
        '''
            Reconstructs list of Waypoint instances from dictionary data.

            :param data: Dictionary containing serialized waypoints.
            :return: List of deserialized Waypoint instances.
        '''
        loaded_pts: list[Waypoint] = []
        raw_list = data.get('waypoints', [])

        if isinstance(raw_list, list):
            for item in raw_list:
                if isinstance(item, dict):
                    loaded_pts.append(cls.deserialize_waypoint(item))

        return loaded_pts

    @classmethod
    def serialize_to_json(
        cls,
        waypoints: Sequence[Waypoint],
        indent: int = 2
    ) -> str:
        '''
            Encodes waypoints sequence into a formatted JSON string.

            :param waypoints: Sequence of Waypoint instances.
            :param indent: JSON indentation level.
            :return: Formatted JSON string.
        '''
        data = cls.serialize_to_dict(waypoints)

        return dumps(data, indent=indent)

    @classmethod
    def deserialize_from_json(cls, json_str: str) -> list[Waypoint]:
        '''
            Decodes JSON string into a list of Waypoint instances.

            :param json_str: JSON-encoded string.
            :return: List of deserialized Waypoint instances.
        '''
        data: dict[str, object] = loads(json_str)

        return cls.deserialize_from_dict(data)
