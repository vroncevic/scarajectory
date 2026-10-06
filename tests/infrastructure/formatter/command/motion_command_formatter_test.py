# -*- coding: UTF-8 -*-

'''
Module
    motion_command_formatter_test.py
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
    Unit testing for MotionCommandFormatter component.
'''

from __future__ import annotations

from unittest import TestCase, main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.formatter.command.motion_command_formatter import MotionCommandFormatter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionCommandFormatterTestCase(TestCase):
    '''Unit tests for MotionCommandFormatter formatting routines.'''

    def test_format_home_and_move(self) -> None:
        '''Verifies format_home and format_move output expected packets.'''
        self.assertEqual(MotionCommandFormatter.format_home(), '<CMD:HOME>')

        pt_custom = Waypoint(x=10.0, y=20.0, z=30.0, speed=50.0, command='<CUSTOM_CMD>')
        self.assertEqual(MotionCommandFormatter.format_move(pt_custom), '<CUSTOM_CMD>')

        pt = Waypoint(x=10.0, y=20.0, z=5.0, speed=50.0, phi=90.0)
        expected_move = '<pt#10.00#20.00#5.00#90.00#50.0#end>'
        self.assertEqual(MotionCommandFormatter.format_move(pt), expected_move)

    def test_format_waypoint_packet(self) -> None:
        '''Verifies packet formatting with zero phi, non-zero phi, and custom command.'''
        pt_zero_phi = Waypoint(x=10.5, y=20.25, z=5.0, speed=40.0, phi=0.0)
        self.assertEqual(
            MotionCommandFormatter.format_waypoint_packet(pt_zero_phi),
            '<pt#10.50#20.25#5.00#40.0#end>',
        )

        pt_rot = Waypoint(x=10.5, y=20.25, z=5.0, speed=40.0, phi=45.0)
        self.assertEqual(
            MotionCommandFormatter.format_waypoint_packet(pt_rot),
            '<pt#10.50#20.25#5.00#45.00#40.0#end>',
        )

        pt_cmd = Waypoint(x=0.0, y=0.0, z=0.0, speed=0.0, command='<CMD:PUMP#1>')
        self.assertEqual(
            MotionCommandFormatter.format_waypoint_packet(pt_cmd),
            '<CMD:PUMP#1>',
        )

    def test_format_program_without_distance(self) -> None:
        '''Verifies format_program stream assembly when total_distance is zero.'''
        waypoints = (
            Waypoint(x=10.0, y=20.0, z=5.0, speed=50.0),
            Waypoint(x=30.0, y=40.0, z=5.0, speed=50.0),
        )
        stream = MotionCommandFormatter.format_program(waypoints)
        self.assertIn('; Total Waypoints: 2', stream)
        self.assertNotIn('; Total Distance:', stream)
        self.assertIn('<CMD:ENABLE>', stream)
        self.assertIn('<pt#10.00#20.00#5.00#50.0#end>', stream)
        self.assertIn('<pt#30.00#40.00#5.00#50.0#end>', stream)

    def test_format_program_with_distance(self) -> None:
        '''Verifies format_program includes distance metric when total_distance > 0.'''
        waypoints = (Waypoint(x=10.0, y=20.0, z=5.0, speed=50.0),)
        stream = MotionCommandFormatter.format_program(waypoints, total_distance=125.456)
        self.assertIn('; Total Distance: 125.46 mm', stream)


if __name__ == '__main__':
    main()
