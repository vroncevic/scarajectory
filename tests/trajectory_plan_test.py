# -*- coding: UTF-8 -*-

'''
Module
    trajectory_plan_test.py
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
    Unit tests for TrajectoryPlan, TrajectoryValidator, and Waypoint serialization with DTOs.
'''

from __future__ import annotations

import os
import sys
import unittest

pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.scara_bounds import ScaraBounds
from scarajectory.core.model.point_dto import PointDTO
from scarajectory.core.model.trajectory_metrics import TrajectoryMetrics
from scarajectory.core.model.trajectory_plan import TrajectoryPlan
from scarajectory.core.service.trajectory_validator import TrajectoryValidator
from scarajectory.core.service.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.communication.transport.serial_transport import SerialTransport
from scarajectory.infrastructure.communication.serial_streamer import SerialStreamer
from scarajectory.core.service.engine import Service
from scarajectory.setup.factory import SCARAjectoryBundleFactory
from scarajectory.engine import SCARAjectory


class TestTrajectoryPlan(unittest.TestCase):
    '''
        Test cases for TrajectoryPlan, TrajectoryValidator, and Service.

        It defines:

            :methods:
                | setUp - Initializes test fixtures.
                | test_add_and_metrics - Tests adding waypoints and computing path distance/time.
                | test_point_dto_conversion - Tests conversion between Waypoint entity and PointDTO.
                | test_validation_pass - Tests reachable points within valid SCARA radius.
                | test_validation_out_of_reach - Tests out of reach points.
                | test_validation_deadzone - Tests deadzone points.
                | test_ascii_generation - Tests ASCII packet format.
                | test_json_persistence - Tests saving and loading JSON plan.
                | test_bundle_factory - Tests ATS bundle creation and engine initialization.
                | test_bundle_factory_custom_geometry - Tests ATS bundle creation with custom kinematic options.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        bounds: ScaraBounds = ScaraBounds(l1=150.0, l2=120.0, z_min=0.0, z_max=100.0)
        self.validator: TrajectoryValidator = TrajectoryValidator(bounds)
        self.transport: SerialTransport = SerialTransport()
        self.streamer: SerialStreamer = SerialStreamer(transport=self.transport)
        self.storage: PlanStorageService = PlanStorageService()
        self.plan: TrajectoryPlan = TrajectoryPlan()
        self.service: Service = Service(validator=self.validator, streamer=self.streamer, storage=self.storage, plan=self.plan)

    def test_add_and_metrics(self) -> None:
        '''
            Tests adding waypoints and computing path distance/time.

            :exceptions: None.
        '''
        p1 = Waypoint(x=150.0, y=0.0, z=20.0, speed=40.0)
        p2 = Waypoint(x=180.0, y=0.0, z=20.0, speed=40.0)
        self.plan.add_point(p1)
        self.plan.add_point(p2)

        self.assertEqual(self.plan.count, 2)
        dist: float = TrajectoryMetrics.calculate_distance(self.plan.waypoints)
        dur: float = TrajectoryMetrics.calculate_duration(self.plan.waypoints)
        self.assertAlmostEqual(dist, 30.0, places=2)
        self.assertAlmostEqual(dur, 0.75, places=2)

    def test_point_dto_conversion(self) -> None:
        '''
            Tests conversion between Waypoint entity and PointDTO.

            :exceptions: None.
        '''
        wp = Waypoint(x=120.0, y=30.0, z=10.0, phi=0.5, speed=50.0, name='P_TEST')
        dto: PointDTO = wp.to_dto()
        self.assertEqual(dto.x, 120.0)
        self.assertEqual(dto.name, 'P_TEST')
        wp_reconstructed = Waypoint.from_dto(dto)
        self.assertEqual(wp, wp_reconstructed)

    def test_validation_pass(self) -> None:
        '''
            Tests valid reachable points.

            :exceptions: None.
        '''
        self.plan.add_point(Waypoint(x=180.0, y=0.0, z=20.0))
        self.plan.add_point(Waypoint(x=150.0, y=50.0, z=10.0))
        valid, msgs = self.service.validate_plan()
        self.assertTrue(valid)

    def test_validation_out_of_reach(self) -> None:
        '''
            Tests out of reach points (> 270 mm).

            :exceptions: None.
        '''
        self.plan.add_point(Waypoint(x=250.0, y=150.0, z=20.0))
        valid, msgs = self.service.validate_plan()
        self.assertFalse(valid)
        self.assertTrue(any('exceeds maximum reach' in m for m in msgs))

    def test_validation_deadzone(self) -> None:
        '''
            Tests deadzone points (< 30 mm).

            :exceptions: None.
        '''
        self.plan.add_point(Waypoint(x=10.0, y=10.0, z=20.0))
        valid, msgs = self.service.validate_plan()
        self.assertFalse(valid)
        self.assertTrue(any('inside deadzone' in m for m in msgs))

    def test_ascii_generation(self) -> None:
        '''
            Tests ASCII packet format.

            :exceptions: None.
        '''
        self.plan.add_point(Waypoint(x=150.0, y=50.0, z=10.0, phi=0.0, speed=40.0))
        program: str = TrajectoryMetrics.to_ascii_program(self.plan.waypoints)
        self.assertIn('<pt#150.00#50.00#10.00#40.0#end>', program)

    def test_json_persistence(self) -> None:
        '''
            Tests saving and loading JSON plan.

            :exceptions: None.
        '''
        tmp_file: str = '/tmp/test_scara_plan.json'
        try:
            self.plan.add_point(Waypoint(x=160.0, y=20.0, z=15.0, phi=1.57, speed=50.0))
            self.service.save_plan(tmp_file)

            new_plan = TrajectoryPlan()
            new_service = Service(validator=self.validator, streamer=self.streamer, storage=self.storage, plan=new_plan)
            new_service.load_plan(tmp_file)
            self.assertEqual(new_plan.count, 1)
            loaded_pt = new_plan.waypoints[0]
            self.assertAlmostEqual(loaded_pt.x, 160.0)
            self.assertAlmostEqual(loaded_pt.y, 20.0)
            self.assertAlmostEqual(loaded_pt.phi, 1.57)
        finally:
            if os.path.exists(tmp_file):
                os.remove(tmp_file)

    def test_bundle_factory(self) -> None:
        '''
            Tests ATS bundle creation and engine initialization.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle()
        engine = SCARAjectory(bundle)
        self.assertTrue(engine.is_initialized())
        service = bundle.service
        bounds = service.get_validator().bounds
        self.assertAlmostEqual(bounds.l1, 150.0)
        self.assertAlmostEqual(bounds.l2, 120.0)

    def test_bundle_factory_custom_geometry(self) -> None:
        '''
            Tests ATS bundle creation with custom kinematic options.

            :exceptions: None.
        '''
        bundle = SCARAjectoryBundleFactory.create_bundle(
            options={
                'l1': 200.0,
                'l2': 180.0,
                'z_min': 5.0,
                'z_max': 250.0,
                'min_speed': 5.0,
                'max_speed': 200.0
            }
        )
        engine = SCARAjectory(bundle)
        self.assertTrue(engine.is_initialized())
        service = bundle.service
        bounds = service.get_validator().bounds
        self.assertAlmostEqual(bounds.l1, 200.0)
        self.assertAlmostEqual(bounds.l2, 180.0)
        self.assertAlmostEqual(bounds.z_max, 250.0)


if __name__ == '__main__':
    unittest.main()
