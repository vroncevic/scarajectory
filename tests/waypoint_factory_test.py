# -*- coding: UTF-8 -*-

'''
Module
    waypoint_factory_test.py
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
    Unit tests for WaypointFactory creation service.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestWaypointFactory(TestCase):
    '''
        Test cases for WaypointFactory creation helper.

        It defines:

            :methods:
                | test_create_minimal - Tests creating Waypoint with only required spatial arguments.
                | test_create_full - Tests creating Waypoint with all explicit arguments.
    '''

    def test_create_minimal(self) -> None:
        '''
            Verifies creation with required x, y, z, speed applying default metadata.
        '''
        pt: Waypoint = WaypointFactory.create(
            x=10.0,
            y=20.0,
            z=30.0,
            speed=40.0,
        )
        self.assertIsInstance(pt, Waypoint)
        self.assertEqual(pt.x, 10.0)
        self.assertEqual(pt.y, 20.0)
        self.assertEqual(pt.z, 30.0)
        self.assertEqual(pt.speed, 40.0)
        self.assertEqual(pt.phi, 0.0)
        self.assertEqual(pt.name, '')
        self.assertEqual(pt.command, '')

    def test_create_full(self) -> None:
        '''
            Verifies creation with full explicit coordinates and metadata attributes.
        '''
        pt: Waypoint = WaypointFactory.create(
            x=150.0,
            y=60.0,
            z=10.0,
            phi=15.0,
            speed=30.0,
            name='WAIT',
            command='<CMD:PUMP#1>',
        )
        self.assertEqual(pt.x, 150.0)
        self.assertEqual(pt.y, 60.0)
        self.assertEqual(pt.z, 10.0)
        self.assertEqual(pt.phi, 15.0)
        self.assertEqual(pt.speed, 30.0)
        self.assertEqual(pt.name, 'WAIT')
        self.assertEqual(pt.command, '<CMD:PUMP#1>')


if __name__ == '__main__':
    main()
