# -*- coding: UTF-8 -*-

'''
Module
    trajectory_serializer_test.py
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
    Unit tests for pure in-memory TrajectorySerializer.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.model.trajectory.trajectory_serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectorySerializer(TestCase):
    '''
        Test cases for in-memory TrajectorySerializer.

        It defines:

            :methods:
                | test_serialize_and_deserialize_dict - Tests dict serialization roundtrip.
                | test_serialize_and_deserialize_json - Tests JSON string serialization roundtrip.
                | test_deserialize_invalid_dict - Tests graceful handling of malformed dictionaries.
    '''

    def test_serialize_and_deserialize_dict(self) -> None:
        '''
            Tests serializing waypoints to dictionary and reconstructing them.
        '''
        pts = [
            Waypoint(x=50.0, y=100.0, z=20.0, phi=0.0, speed=40.0, name='Start'),
            Waypoint(x=150.0, y=100.0, z=20.0, phi=0.0, speed=40.0, name='End')
        ]
        data = TrajectorySerializer.serialize_to_dict(pts)
        self.assertIn('version', data)
        self.assertIn('waypoints', data)
        self.assertEqual(len(data['waypoints']), 2)

        loaded_pts = TrajectorySerializer.deserialize_from_dict(data)
        self.assertEqual(len(loaded_pts), 2)
        self.assertEqual(loaded_pts[0].x, 50.0)
        self.assertEqual(loaded_pts[1].x, 150.0)
        self.assertEqual(loaded_pts[0].name, 'Start')

    def test_serialize_and_deserialize_json(self) -> None:
        '''
            Tests serializing waypoints to JSON string and parsing back.
        '''
        pts = [
            Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='P1')
        ]
        json_str = TrajectorySerializer.serialize_to_json(pts)
        self.assertIsInstance(json_str, str)
        self.assertIn('"waypoints"', json_str)

        loaded_pts = TrajectorySerializer.deserialize_from_json(json_str)
        self.assertEqual(len(loaded_pts), 1)
        self.assertEqual(loaded_pts[0].x, 10.0)
        self.assertEqual(loaded_pts[0].name, 'P1')

    def test_deserialize_invalid_dict(self) -> None:
        '''
            Tests deserializing when waypoints key is missing or not a list.
        '''
        self.assertEqual(TrajectorySerializer.deserialize_from_dict({}), [])
        self.assertEqual(
            TrajectorySerializer.deserialize_from_dict({'waypoints': 'invalid'}),
            []
        )


if __name__ == '__main__':
    main()
