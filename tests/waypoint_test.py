# -*- coding: UTF-8 -*-

'''
Module
    waypoint_test.py
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
    Unit tests for Waypoint entity.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.communication.protocol.motion_command_formatter import (
    MotionCommandFormatter
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypoint(TestCase):
    '''
        Test cases for Waypoint data class and DTO conversion.

        It defines:

            :methods:
                | test_waypoint_creation - Tests instantiation and property access of Waypoint.
                | test_waypoint_equality - Tests equality and string representation.
    '''

    def test_waypoint_creation(self) -> None:
        '''
            Tests instantiation and default values of Waypoint.

            :exceptions: None.
        '''
        pt = Waypoint(x=100.5, y=50.2, z=15.0, phi=45.0, speed=35.0, name='P1')
        self.assertEqual(pt.x, 100.5)
        self.assertEqual(pt.y, 50.2)
        self.assertEqual(pt.z, 15.0)
        self.assertEqual(pt.phi, 45.0)
        self.assertEqual(pt.speed, 35.0)
        self.assertEqual(pt.name, 'P1')


    def test_waypoint_equality(self) -> None:
        '''
            Tests equality comparison between Waypoint instances.

            :exceptions: None.
        '''
        pt1 = Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='A')
        pt2 = Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='A')
        pt3 = Waypoint(x=10.0, y=20.0, z=30.0, phi=0.0, speed=50.0, name='B')
        self.assertEqual(pt1, pt2)
        self.assertNotEqual(pt1, pt3)

    def test_waypoint_command_packet(self) -> None:
        '''
            Tests packet generation with and without raw command attribute via formatter.
        '''
        pt_move = Waypoint(x=100.0, y=50.0, z=20.0, phi=0.0, speed=40.0)
        self.assertEqual(
            MotionCommandFormatter.format_move(pt_move),
            '<pt#100.00#50.00#20.00#0.00#40.0#end>'
        )

        pt_cmd = Waypoint(x=100.0, y=50.0, z=20.0, command='<CMD:WAIT#500>')
        self.assertEqual(
            MotionCommandFormatter.format_move(pt_cmd),
            '<CMD:WAIT#500>'
        )

    def test_waypoint_dict_serialization(self) -> None:
        '''
            Tests dictionary serialization and deserialization with command.
        '''
        pt = Waypoint(x=150.0, y=60.0, z=10.0, phi=15.0, speed=30.0, name='WAIT', command='<CMD:PUMP#1>')
        data = pt.to_dict()
        self.assertEqual(data.get('command'), '<CMD:PUMP#1>')
        restored = Waypoint.from_dict(data)
        self.assertEqual(restored.command, '<CMD:PUMP#1>')
        self.assertEqual(restored.x, 150.0)


if __name__ == '__main__':
    main()
