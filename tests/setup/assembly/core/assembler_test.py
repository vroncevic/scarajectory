# -*- coding: UTF-8 -*-

'''
Module
    assembler_test.py
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
    Unit tests for AppCoreAssembler.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaralang.core.model.kinematics.profile.bounds import ScaraBounds
from scarajectory.infrastructure.settings.dependencies import SettingsDependencies
from scarajectory.infrastructure.settings.factory import SettingsFactory
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.setup.assembly.core.assembler import AppCoreAssembler
from scarajectory.setup.assembly.core.bundle import AppCoreBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class AppCoreAssemblerTest(TestCase):
    '''
        Test suite verifying AppCoreAssembler behavior.

        It defines:

            :methods:
                | setUp - Initializes test fixtures and loads ScaraBounds.
                | test_assemble_core_bundle - Tests assembly of core bundle.
                | test_get_version - Tests assembler version query.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixtures.

            :exceptions: None.
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

    def test_assemble_core_bundle(self) -> None:
        '''
            Tests assembly of core bundle.

            :exceptions: None.
        '''
        bundle: AppCoreBundle = AppCoreAssembler.assemble(
            bounds=self.bounds,
            context_bundle=ContextBundleFactory.create_bundle(),
        )
        self.assertIsInstance(bundle, AppCoreBundle)
        self.assertEqual(bundle.bounds.links.l1, self.bounds.links.l1)
        self.assertEqual(bundle.bounds.links.l2, self.bounds.links.l2)
        self.assertIsNotNone(bundle.transmission)
        self.assertIsNotNone(bundle.kinematics)
        self.assertIsNotNone(bundle.validator)
        self.assertIsNotNone(bundle.avoidance_adapter)
        self.assertIsNotNone(bundle.planner_adapter)
        self.assertIsNotNone(bundle.boundary_adapter)
        self.assertGreater(bundle.validator.r_max, bundle.validator.r_min)

    def test_get_version(self) -> None:
        '''
            Tests assembler version query.

            :exceptions: None.
        '''
        version: str = AppCoreAssembler.get_version()
        self.assertIsInstance(version, str)
        self.assertTrue(len(version) > 0)


if __name__ == '__main__':
    main()
