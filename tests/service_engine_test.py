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

from os import remove
from os.path import abspath, dirname, exists
from sys import path
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.service.trajectory.discretization.waypoint_factory import WaypointFactory
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.trajectory.plan.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scarajectory.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory
from scarajectory.infrastructure.storage.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory
from scarajectory.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scarajectory.core.service.service_factory import ServiceFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestServiceEngine(TestCase):
    '''
        Test cases for Service business facade.

        It defines:

            :methods:
                | setUp - Initializes service fixtures.
                | test_service_initialization - Tests accessor methods and initialization flag.
                | test_save_and_load_plan - Tests facade plan saving and loading.
                | test_plan_facade_methods - Tests facade plan operations (clear, undo, redo, new_plan).
                | test_streaming_facade_methods - Tests facade streaming operations (pause, resume, stop).
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        loader = ScaraConfigLoaderFactory.create()
        self.bounds = loader.load_bounds_with_options(
            options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        )
        self.kinematics = KinematicsServiceFactory.create(bounds=self.bounds)
        self.validator = TrajectoryValidatorFactory.create(kinematics=self.kinematics)
        self.storage = PlanStorageService()
        self.streamer = TrajectoryStreamerFactory.create_default()
        self.plan = TrajectoryPlanFactory.create()
        transmission = loader.load_transmission()
        self.dsl_service = ScaraDslServiceFactory.create(
            validator=self.validator,
            kinematics=self.validator.kinematics,
            transmission=transmission,
        )
        self.service = ServiceFactory.create(
            validator=self.validator,
            streamer=self.streamer,
            storage=self.storage,
            plan=self.plan,
            dsl_service=self.dsl_service,
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
        self.assertEqual(self.service.get_dsl_service(), self.dsl_service)

    def test_save_and_load_plan(self) -> None:
        '''
            Tests save_plan and load_plan facade integration.

            :exceptions: None.
        '''
        pt = WaypointFactory.create(x=100.0, y=50.0, z=20.0, phi=0.0, speed=40.0)
        self.plan.add_point(pt)

        with NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path = tf.name

        try:
            self.service.save_plan(tmp_path)

            self.plan.clear()
            self.assertEqual(self.plan.count, 0)

            self.service.load_plan(tmp_path)
            self.assertEqual(self.plan.count, 1)
            self.assertEqual(self.plan.waypoints[0].x, 100.0)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_plan_facade_methods(self) -> None:
        '''
            Tests clear_plan, undo, redo, and new_plan facade methods.

            :exceptions: None.
        '''
        pt1 = WaypointFactory.create(x=50.0, y=20.0, z=10.0, phi=0.0, speed=20.0)
        pt2 = WaypointFactory.create(x=80.0, y=40.0, z=15.0, phi=5.0, speed=30.0)

        self.plan.add_point(pt1)
        self.plan.add_point(pt2)
        self.assertEqual(self.plan.count, 2)

        undone = self.service.undo()
        self.assertTrue(undone)
        self.assertEqual(self.plan.count, 1)

        redone = self.service.redo()
        self.assertTrue(redone)
        self.assertEqual(self.plan.count, 2)

        self.service.clear_plan()
        self.assertEqual(self.plan.count, 0)

        self.plan.add_point(pt1)
        self.assertEqual(self.plan.count, 1)
        self.service.new_plan()
        self.assertEqual(self.plan.count, 0)

    def test_streaming_facade_methods(self) -> None:
        '''
            Tests streamer access via get_streamer.

            :exceptions: None.
        '''
        streamer = self.service.get_streamer()
        streamer.pause_streaming()
        streamer.resume_streaming()
        streamer.stop_streaming()


if __name__ == '__main__':
    main()
