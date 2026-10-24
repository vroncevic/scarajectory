# -*- coding: UTF-8 -*-

'''
Module
    adapter_test.py
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
    Unit tests for TrajectoryValidationAdapter.
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

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.core.service.trajectory.plan.store.dependencies import StoreDependencies
from scarajectory.core.service.trajectory.plan.store.factory import StoreFactory
from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
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


class TestTrajectoryValidationAdapter(TestCase):
    '''
    Test cases for TrajectoryValidationAdapter.

    It defines:

        :methods:
            | setUp - Initializes test fixtures and adapter.
            | test_structural_conformance - Verifies ITrajectoryValidator conformance.
            | test_properties - Verifies reach boundaries and bounds properties.
            | test_validate_point - Tests waypoint reachability validation.
            | test_validate_plan - Tests full plan validation.
            | test_validate_plan_dual_elbow_warnings - Tests dual elbow warnings.
    '''

    def setUp(self) -> None:
        '''
        Sets up test fixtures and instantiates TrajectoryValidationAdapter.
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
        self.bounds: ScaraBounds = (
            settings_provides.bounds_provides.bounds_loader.load_bounds_with_options(
                options={'l1': 150.0, 'l2': 120.0, 'z_min': 0.0, 'z_max': 100.0}
            )
        )
        kinematics: KinematicsProvides = KinematicsFactory.create(
            dependencies=KinematicsDependencies(
                bounds=self.bounds,
                dls_config=DefaultScaraProfile.create_dls_config(),
            )
        )
        validation: ValidationProvides = ValidationFactory.create(
            dependencies=ValidationDependencies(
                workspace=kinematics.workspace,
                envelope=kinematics.envelope,
            )
        )
        self.adapter: TrajectoryValidationAdapter = (
            TrajectoryValidationAdapterFactory.create(
                dependencies=TrajectoryValidationDependencies(
                    workspace_envelope=kinematics.envelope,
                    waypoint_validator=validation.waypoint,
                    plan_validator=validation.plan,
                )
            )
        )

    def test_structural_conformance(self) -> None:
        '''
        Verifies that TrajectoryValidationAdapter structurally satisfies ITrajectoryValidator.
        '''
        self.assertIsInstance(self.adapter, ITrajectoryValidator)

    def test_properties(self) -> None:
        '''
        Verifies adapter exposes reach boundaries and bounds.
        '''
        self.assertGreater(self.adapter.r_max, self.adapter.r_min)
        self.assertEqual(self.adapter.bounds, self.bounds)

    def test_validate_point(self) -> None:
        '''
        Tests reachable and out-of-reach waypoint validation.
        '''
        reachable = TrajectoryWaypoint(
            x=100.0, y=100.0, z=20.0, speed=50.0, phi=0.0, name='', command=''
        )
        self.assertTrue(self.adapter.validate_point(reachable).is_valid)

        lefty_only = TrajectoryWaypoint(
            x=-120.0, y=-120.0, z=20.0, speed=50.0, phi=0.0, name='', command=''
        )
        self.assertTrue(self.adapter.validate_point(lefty_only).is_valid)

        out_of_reach = TrajectoryWaypoint(
            x=500.0, y=500.0, z=20.0, speed=50.0, phi=0.0, name='', command=''
        )
        self.assertFalse(self.adapter.validate_point(out_of_reach).is_valid)

        both_invalid = TrajectoryWaypoint(
            x=-250.0, y=-100.0, z=20.0, speed=50.0, phi=0.0, name='', command=''
        )
        self.assertFalse(self.adapter.validate_point(both_invalid).is_valid)

    def test_validate_plan(self) -> None:
        '''
        Tests plan validation with store waypoints.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        pt = TrajectoryWaypoint(x=100.0, y=100.0, z=20.0, speed=50.0, phi=0.0, name='', command='')
        store.add(pt)
        is_valid, _ = self.adapter.validate_plan(store)
        self.assertTrue(is_valid)

        empty_store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        is_empty_valid, empty_msgs = self.adapter.validate_plan(empty_store)
        self.assertFalse(is_empty_valid)
        self.assertIn('Trajectory plan is empty', empty_msgs[0])

        out_store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        out_store.add(
            TrajectoryWaypoint(x=500.0, y=500.0, z=20.0, speed=50.0, phi=0.0, name='', command='')
        )
        is_out_valid, _ = self.adapter.validate_plan(out_store)
        self.assertFalse(is_out_valid)

        both_store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        both_store.add(
            TrajectoryWaypoint(x=-250.0, y=-100.0, z=20.0, speed=50.0, phi=0.0, name='', command='')
        )
        is_both_valid, both_msgs = self.adapter.validate_plan(both_store)
        self.assertFalse(is_both_valid)
        self.assertTrue(any('violates J1 limits in both configurations' in m for m in both_msgs))

    def test_validate_plan_dual_elbow_warnings(self) -> None:
        '''
        Tests plan validation generates dual-elbow warning for bottom quadrant waypoint.
        '''
        store = StoreFactory.create(
            StoreDependencies(initial_waypoints=())
        ).waypoint_store
        pt = TrajectoryWaypoint(x=-23.0, y=-88.0, z=20.0, speed=50.0, phi=0.0, name='', command='')
        store.add(pt)
        is_valid, msgs = self.adapter.validate_plan(store)
        self.assertTrue(is_valid)
        self.assertTrue(any('requires Lefty elbow configuration' in m for m in msgs))


if __name__ == '__main__':
    main()
