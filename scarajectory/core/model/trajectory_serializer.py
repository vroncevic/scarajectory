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
    Serializes and deserializes trajectory plans to and from JSON format.
'''

from __future__ import annotations

import json
from collections.abc import Sequence

from scarajectory.core.model.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TrajectorySerializer:
    '''
        Serializes and deserializes trajectory plans to and from JSON format.

        It defines:

            :methods:
                | save_json - Saves waypoints sequence to JSON file.
                | load_json - Loads waypoints sequence from JSON file.
    '''

    @staticmethod
    def save_json(waypoints: Sequence[Waypoint], filepath: str) -> None:
        '''
            Saves waypoints sequence to JSON file.

            :param waypoints: Sequence of waypoints.
            :param filepath: Target destination file path.
            :exceptions: OSError, json.JSONDecodeError.
        '''
        data: dict[str, object] = {
            'version': '1.0.2',
            'waypoints': [pt.to_dict() for pt in waypoints]
        }
        with open(filepath, 'w', encoding='utf-8') as file_handle:
            json.dump(data, file_handle, indent=2)

    @staticmethod
    def load_json(filepath: str) -> list[Waypoint]:
        '''
            Loads waypoints sequence from JSON file.

            :param filepath: Source file path.
            :return: List of loaded Waypoint instances.
            :exceptions: OSError, json.JSONDecodeError.
        '''
        with open(filepath, 'r', encoding='utf-8') as file_handle:
            data: dict[str, object] = json.load(file_handle)
        loaded_pts: list[Waypoint] = []
        raw_list = data.get('waypoints', [])
        if isinstance(raw_list, list):
            for item in raw_list:
                if isinstance(item, dict):
                    loaded_pts.append(Waypoint.from_dict(item))
        return loaded_pts
