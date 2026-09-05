# -*- coding: UTF-8 -*-

'''
Module
    service_engine_test.py
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
    Unit tests for core Service facade engine.
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
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory_validator import TrajectoryValidator
from scarajectory.core.service.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
from scarajectory.infrastructure.communication.serial_streamer import SerialStreamer
from scarajectory.core.service.engine import Service

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServiceEngine(unittest.TestCase):
    '''
        Test cases for Service business facade.

        It defines:

            :methods:
                | setUp - Initializes service fixtures.
                | test_service_initialization - Tests accessor methods and initialization flag.
                | test_save_and_load_plan - Tests facade plan saving and loading.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        self.bounds = ScaraBounds(l1=150.0, l2=120.0, z_min=0.0, z_max=100.0)
        self.validator = TrajectoryValidator(self.bounds)
        self.storage = PlanStorageService()
        self.streamer = SerialStreamer(SerialTransport())
        self.plan = TrajectoryPlan()
        self.service = Service(
            validator=self.validator,
            streamer=self.streamer,
            storage=self.storage,
            plan=self.plan
        )

    def test_service_initialization(self) -> None:
        '''
            Tests getters and initialization.

            :exceptions: None.
        '''
        self.assertTrue(self.service.is_initialized())
        self.assertEqual(self.service.get_plan(), self.plan)
        self.assertEqual(self.service.get_validator(), self.validator)
        self.assertEqual(self.service.get_storage(), self.storage)
        self.assertEqual(self.service.get_streamer(), self.streamer)

    def test_save_and_load_plan(self) -> None:
        '''
            Tests save_plan and load_plan facade integration.

            :exceptions: None.
        '''
        pt = Waypoint(x=100.0, y=50.0, z=20.0, phi=0.0, speed=40.0)
        self.plan.add_point(pt)

        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path = tf.name

        try:
            self.service.save_plan(tmp_path)

            self.plan.clear()
            self.assertEqual(self.plan.count, 0)

            self.service.load_plan(tmp_path)
            self.assertEqual(self.plan.count, 1)
            self.assertEqual(self.plan.waypoints[0].x, 100.0)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == '__main__':
    unittest.main()
