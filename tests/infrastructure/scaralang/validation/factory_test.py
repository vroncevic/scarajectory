# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for TrajectoryValidationAdapterFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scaralang.core.service.kinematics.dependencies import KinematicsDependencies
from scaralang.core.service.kinematics.factory import KinematicsFactory
from scaralang.core.service.kinematics.profile.default_scara_profile import DefaultScaraProfile
from scaralang.core.service.kinematics.provides import KinematicsProvides
from scaralang.core.service.trajectory.validation.dependencies import ValidationDependencies
from scaralang.core.service.trajectory.validation.factory import ValidationFactory
from scaralang.core.service.trajectory.validation.provides import ValidationProvides

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.scaralang.validation.adapter import TrajectoryValidationAdapter
from scarajectory.infrastructure.scaralang.validation.dependencies import TrajectoryValidationDependencies
from scarajectory.infrastructure.scaralang.validation.factory import TrajectoryValidationAdapterFactory
from scarajectory.infrastructure.settings.dependencies import SettingsDependencies
from scarajectory.infrastructure.settings.factory import SettingsFactory
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTrajectoryValidationAdapterFactory(TestCase):
    '''
    Test cases for TrajectoryValidationAdapterFactory.

    It defines:

        :methods:
            | setUp - Prepares test dependencies.
            | test_create - Verifies factory produces TrajectoryValidationAdapter instance.
            | test_get_version - Verifies factory semantic version string.
    '''

    def setUp(self) -> None:
        '''
        Sets up test dependencies.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=bundle)
        )
        settings_provides = SettingsFactory.create(
            SettingsDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        bounds: ScaraBounds = (
            settings_provides.bounds_provides.bounds_loader.load_bounds_with_options(
                options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
            )
        )
        kinematics: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        validation: ValidationProvides = ValidationFactory.create(
            dependencies=ValidationDependencies(
                workspace=kinematics.workspace,
                envelope=kinematics.envelope,
            )
        )
        self.dependencies = TrajectoryValidationDependencies(
            workspace_envelope=kinematics.envelope,
            waypoint_validator=validation.waypoint,
            plan_validator=validation.plan,
        )

    def test_create(self) -> None:
        '''
        Verifies that create returns TrajectoryValidationAdapter instance.
        '''
        adapter = TrajectoryValidationAdapterFactory.create(
            dependencies=self.dependencies
        )
        self.assertIsInstance(adapter, TrajectoryValidationAdapter)

    def test_get_version(self) -> None:
        '''
        Verifies that get_version returns non-empty string.
        '''
        self.assertTrue(bool(TrajectoryValidationAdapterFactory.get_version()))


if __name__ == '__main__':
    main()
