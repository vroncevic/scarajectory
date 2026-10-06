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
from os.path import exists
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.core.service.service_factory import ServiceFactory
from scarajectory.core.service.trajectory.history.plan_history_factory import PlanHistoryFactory
from scarajectory.core.service.trajectory.plan.mutation.plan_mutation_service_factory import PlanMutationServiceFactory
from scarajectory.core.service.trajectory.plan.observer.plan_observer_dispatcher_factory import PlanObserverDispatcherFactory
from scarajectory.core.service.trajectory.plan.selection.plan_selection_manager_factory import PlanSelectionManagerFactory
from scarajectory.core.service.trajectory.plan.store.waypoint_store_factory import WaypointStoreFactory
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory

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
                | test_plan_facade_methods - Tests facade clear_plan and validate_plan.
    '''

    def setUp(self) -> None:
        '''
            Initializes test fixtures.

            :exceptions: None.
        '''
        bounds = ScaraBoundsLoaderFactory.create().load_bounds_with_options(
            options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        )
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        self.validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        self.storage = PlanStorageServiceFactory.create()
        self.store = WaypointStoreFactory.create()
        self.history_storage = PlanHistoryFactory.create()
        self.selection_mgr = PlanSelectionManagerFactory.create()
        self.dispatcher = PlanObserverDispatcherFactory.create()
        self.mutation = PlanMutationServiceFactory.create(
            store=self.store,
            history=self.history_storage,
            selection=self.selection_mgr,
            dispatcher=self.dispatcher,
        )
        self.service = ServiceFactory.create(
            validator=self.validator,
            storage=self.storage,
            store=self.store,
            mutation=self.mutation,
        )

    def test_service_initialization(self) -> None:
        '''
            Tests getters and initialization.

            :exceptions: None.
        '''
        self.assertTrue(self.service.is_initialized())
        self.assertEqual(self.service.validator, self.validator)

    def test_save_and_load_plan(self) -> None:
        '''
            Tests save_plan and load_plan facade integration.

            :exceptions: None.
        '''
        pt = Waypoint(x=100.0, y=50.0, z=20.0, phi=0.0, speed=40.0)
        self.mutation.add_point(pt)

        with NamedTemporaryFile(suffix='.json', delete=False) as tf:
            tmp_path = tf.name

        try:
            self.service.save_plan(tmp_path)

            self.mutation.clear()
            self.assertEqual(self.store.count, 0)

            self.service.load_plan(tmp_path)
            self.assertEqual(self.store.count, 1)
            self.assertEqual(self.store.waypoints[0].x, 100.0)
        finally:
            if exists(tmp_path):
                remove(tmp_path)

    def test_plan_facade_methods(self) -> None:
        '''
            Tests clear_plan and validate_plan facade methods.

            :exceptions: None.
        '''
        pt1 = Waypoint(x=100.0, y=100.0, z=20.0, phi=0.0, speed=40.0)
        pt2 = Waypoint(x=120.0, y=120.0, z=20.0, phi=0.0, speed=40.0)

        self.mutation.add_point(pt1)
        self.mutation.add_point(pt2)
        self.assertEqual(self.store.count, 2)

        valid, msgs = self.service.validate_plan()
        self.assertTrue(valid)
        self.assertGreater(len(msgs), 0)

        self.service.clear_plan()
        self.assertEqual(self.store.count, 0)


if __name__ == '__main__':
    main()
