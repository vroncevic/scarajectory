# -*- coding: UTF-8 -*-

'''
Module
    plan_storage_service_test.py
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
    Unit tests for PlanStorageService JSON file persistence.
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
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.plan_storage_service import PlanStorageService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestPlanStorageService(unittest.TestCase):
    '''
        Test cases for PlanStorageService disk operations.

        It defines:

            :methods:
                | test_save_and_load_plan - Tests writing and reading trajectory JSON file.
    '''

    def test_save_and_load_plan(self) -> None:
        '''
            Tests roundtrip file storage and retrieval.

            :exceptions: None.
        '''
        storage = PlanStorageService()
        plan = TrajectoryPlan()
        plan.add_point(Waypoint(x=50.0, y=60.0, z=20.0, phi=0.0, speed=30.0, name='P1'))
        plan.add_point(Waypoint(x=70.0, y=80.0, z=20.0, phi=0.0, speed=30.0, name='P2'))

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path = tf.name

        try:
            storage.save_plan(plan, tmp_path)
            loaded_pts = storage.load_plan(tmp_path)
            self.assertEqual(len(loaded_pts), 2)
            self.assertEqual(loaded_pts[0].x, 50.0)
            self.assertEqual(loaded_pts[1].x, 70.0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == '__main__':
    unittest.main()
