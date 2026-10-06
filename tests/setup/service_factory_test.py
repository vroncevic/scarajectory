# -*- coding: UTF-8 -*-

'''
Module
    service_factory_test.py
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
    Unit tests for ServiceFactory assembly service.
'''

from __future__ import annotations

from unittest import TestCase
from unittest import main

from scaralang.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory
from scaralang.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.core.service.engine import Service
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


class TestServiceFactory(TestCase):
    '''
        Test cases for ServiceFactory assembly.

        It defines:

            :methods:
                | test_create_service - Verifies assembling and creating a Service instance.
    '''

    def test_create_service(self) -> None:
        '''
            Verifies that ServiceFactory creates a valid, initialized Service.

            :exceptions: None.
        '''
        bounds = ScaraBoundsLoaderFactory.create().load_bounds_with_options(
            options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        )
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        storage = PlanStorageServiceFactory.create()
        store = WaypointStoreFactory.create()
        history_storage = PlanHistoryFactory.create()
        selection_mgr = PlanSelectionManagerFactory.create()
        dispatcher = PlanObserverDispatcherFactory.create()
        mutation = PlanMutationServiceFactory.create(
            store=store,
            history=history_storage,
            selection=selection_mgr,
            dispatcher=dispatcher,
        )

        service: Service = ServiceFactory.create(
            validator=validator,
            storage=storage,
            store=store,
            mutation=mutation,
        )

        self.assertIsInstance(service, Service)
        self.assertTrue(service.is_initialized())
        self.assertEqual(service.validator, validator)

    def test_get_version(self) -> None:
        '''
            Verifies factory version string.

            :exceptions: None.
        '''
        version = ServiceFactory.get_version()
        self.assertTrue(isinstance(version, str) and len(version) > 0)


if __name__ == '__main__':
    main()
