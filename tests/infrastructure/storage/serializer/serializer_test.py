# -*- coding: UTF-8 -*-

'''
Module
    serializer_test.py
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

from unittest import TestCase

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.storage.serializer.serializer import TrajectorySerializer

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
                | test_serialize_and_deserialize_waypoint - Round-trip for single TrajectoryWaypoint.
                | test_serialize_and_deserialize_dict - Round-trip for TrajectoryWaypoint sequence via dict.
                | test_serialize_and_deserialize_json - Round-trip for TrajectoryWaypoint sequence via JSON string.
                | test_deserialize_malformed - Edge cases for malformed inputs.
    '''

    def test_serialize_and_deserialize_waypoint(self) -> None:
        '''Tests round-trip serialization of single TrajectoryWaypoint.'''
        pt = TrajectoryWaypoint(
            x=150.1234,
            y=-50.5678,
            z=12.0,
            phi=45.5,
            speed=30.0,
            name='pt1',
            command='TEST'
        )
        data = TrajectorySerializer.serialize_waypoint(pt)
        self.assertEqual(data['x'], 150.123)
        self.assertEqual(data['y'], -50.568)
        self.assertEqual(data['name'], 'pt1')

        restored = TrajectorySerializer.deserialize_waypoint(data)
        self.assertAlmostEqual(restored.x, 150.123, places=3)
        self.assertAlmostEqual(restored.y, -50.568, places=3)
        self.assertEqual(restored.name, 'pt1')
        self.assertEqual(restored.command, 'TEST')

    def test_serialize_and_deserialize_dict(self) -> None:
        '''Tests round-trip serialization of waypoints list via dictionary.'''
        pts = [
            TrajectoryWaypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='a', command='C1'),
            TrajectoryWaypoint(x=40.0, y=50.0, z=60.0, phi=10.0, speed=60.0, name='b', command='C2'),
        ]
        data = TrajectorySerializer.serialize_to_dict(pts)
        self.assertIn('version', data)
        self.assertIn('waypoints', data)
        self.assertEqual(len(data['waypoints']), 2)

        loaded_pts = TrajectorySerializer.deserialize_from_dict(data)
        self.assertEqual(len(loaded_pts), 2)
        self.assertEqual(loaded_pts[0].name, 'a')
        self.assertEqual(loaded_pts[1].name, 'b')

    def test_serialize_and_deserialize_json(self) -> None:
        '''Tests round-trip serialization of waypoints list via JSON string.'''
        pts = [
            TrajectoryWaypoint(x=1.0, y=2.0, z=3.0, phi=4.0, speed=5.0, name='p1', command=''),
            TrajectoryWaypoint(x=6.0, y=7.0, z=8.0, phi=9.0, speed=10.0, name='p2', command=''),
        ]
        json_str = TrajectorySerializer.serialize_to_json(pts)
        self.assertIsInstance(json_str, str)
        self.assertIn('"version": "1.0.0"', json_str)

        loaded_pts = TrajectorySerializer.deserialize_from_json(json_str)
        self.assertEqual(len(loaded_pts), 2)
        self.assertEqual(loaded_pts[0].name, 'p1')
        self.assertEqual(loaded_pts[1].name, 'p2')

    def test_deserialize_malformed(self) -> None:
        '''Tests robust handling of malformed input data.'''
        self.assertEqual(TrajectorySerializer.deserialize_from_dict({}), [])
        self.assertEqual(
            TrajectorySerializer.deserialize_from_dict({'waypoints': 'invalid'}),
            []
        )
        self.assertEqual(TrajectorySerializer.deserialize_from_json(''), [])
        self.assertEqual(TrajectorySerializer.deserialize_from_json('invalid json'), [])
        self.assertEqual(TrajectorySerializer.deserialize_from_json('123'), [])
