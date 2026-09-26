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

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.service.service_factory import ServiceFactory
from scarajectory.core.service.engine import Service
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory
from scarajectory.core.service.trajectory.validation.trajectory_validator_factory import TrajectoryValidatorFactory
from scarajectory.infrastructure.communication.streamer.trajectory_streamer_factory import TrajectoryStreamerFactory
from scarajectory.infrastructure.storage.plan_storage_service_factory import PlanStorageServiceFactory
from scarajectory.core.service.trajectory.plan.trajectory_plan_factory import TrajectoryPlanFactory
from scaralang.core.service.dsl.scara_dsl_service_factory import ScaraDslServiceFactory
from scarajectory.core.service.kinematics.kinematics_service_factory import KinematicsServiceFactory

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
        loader = ScaraConfigLoaderFactory.create()
        bounds = loader.load_bounds_with_options(
            options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
        )
        kinematics = KinematicsServiceFactory.create(bounds=bounds)
        validator = TrajectoryValidatorFactory.create(kinematics=kinematics)
        streamer = TrajectoryStreamerFactory.create_default()
        storage = PlanStorageServiceFactory.create()
        plan = TrajectoryPlanFactory.create()
        transmission = loader.load_transmission()
        dsl_service = ScaraDslServiceFactory.create(
            validator=validator,
            kinematics=validator.kinematics,
            transmission=transmission,
        )

        service: Service = ServiceFactory.create(
            validator=validator,
            streamer=streamer,
            storage=storage,
            plan=plan,
            dsl_service=dsl_service,
        )

        self.assertIsInstance(service, Service)
        self.assertTrue(service.is_initialized())
        self.assertEqual(service.get_plan(), plan)
        self.assertEqual(service.get_validator(), validator)
        self.assertEqual(service.get_storage(), storage)
        self.assertEqual(service.get_streamer(), streamer)
        self.assertEqual(service.get_dsl_service(), dsl_service)


if __name__ == '__main__':
    main()
