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
    Unit tests for TrajectorySerializer.
'''

from __future__ import annotations

import os
import sys
import tempfile
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.trajectory_serializer import TrajectorySerializer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectorySerializer(unittest.TestCase):
    '''
        Test cases for TrajectorySerializer.

        It defines:

            :methods:
                | test_save_and_load_json - Tests saving and loading waypoints to/from JSON file.
    '''

    def test_save_and_load_json(self) -> None:
        '''
            Tests serializing and deserializing waypoints JSON file.

            :exceptions: None.
        '''
        pts = [
            Waypoint(x=50.0, y=100.0, z=20.0, phi=0.0, speed=40.0, name='Start'),
            Waypoint(x=150.0, y=100.0, z=20.0, phi=0.0, speed=40.0, name='End')
        ]
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path = tf.name

        try:
            TrajectorySerializer.save_json(pts, tmp_path)
            loaded_pts = TrajectorySerializer.load_json(tmp_path)
            self.assertEqual(len(loaded_pts), 2)
            self.assertEqual(loaded_pts[0].x, 50.0)
            self.assertEqual(loaded_pts[1].x, 150.0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == '__main__':
    unittest.main()
