# -*- coding: UTF-8 -*-

'''
Module
    loader_test.py
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
    Unit tests for ScaraBoundsLoader.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scaralang.core.model.kinematics.profile.bounds import ScaraBounds

from scarajectory.infrastructure.settings.bounds.loader.loader import ScaraBoundsLoader
from scarajectory.infrastructure.settings.bounds.parser.parser import ScaraBoundsParser
from scarajectory.infrastructure.settings.reader.dependencies import ReaderDependencies
from scarajectory.infrastructure.settings.reader.factory import ReaderFactory
from scarajectory.infrastructure.settings.reader.provides import ReaderProvides
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


class TestScaraBoundsLoader(TestCase):
    '''
        Unit test cases verifying ScaraBoundsLoader operations.

        It defines:

            :methods:
                | setUp - Initializes loader fixture.
                | test_load_bounds - Verifies bounds creation from JSON configuration.
                | test_load_bounds_with_options - Verifies override options in bounds creation.
    '''

    loader: ScaraBoundsLoader

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing ScaraBoundsLoader.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=bundle)
        )
        reader_provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        self.loader = ScaraBoundsLoader(
            settings_reader=reader_provides.settings_reader,
            bounds_parser=ScaraBoundsParser(),
        )

    def test_load_bounds(self) -> None:
        '''
            Verifies load_bounds returns pure ScaraBounds populated from JSON configuration.
        '''
        bounds: ScaraBounds = self.loader.load_bounds()
        self.assertIsInstance(bounds, ScaraBounds)
        self.assertEqual(bounds.links.l1, 150.0)
        self.assertEqual(bounds.links.l2, 120.0)
        self.assertEqual(bounds.vertical.z_min, 0.0)
        self.assertEqual(bounds.vertical.z_max, 100.0)
        self.assertEqual(bounds.speeds.default_speed, 50.0)
        self.assertGreater(bounds.singularity.deadzone_r_min, 0.0)

    def test_load_bounds_with_options(self) -> None:
        '''
            Verifies options override values from JSON configuration in bounds.
        '''
        bounds: ScaraBounds = self.loader.load_bounds_with_options(
            options={'l1': 160.0, 'l2': 130.0, 'default_speed': 60.0}
        )
        self.assertEqual(bounds.links.l1, 160.0)
        self.assertEqual(bounds.links.l2, 130.0)
        self.assertEqual(bounds.speeds.default_speed, 60.0)


if __name__ == '__main__':
    main()
