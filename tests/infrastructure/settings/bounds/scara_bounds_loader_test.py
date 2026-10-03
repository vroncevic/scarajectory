# -*- coding: UTF-8 -*-

'''
Module
    scara_bounds_loader_test.py
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
    Unit tests for ScaraBoundsLoader and ScaraBoundsLoaderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scaralang.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.service.settings.iscara_bounds_loader import IScaraBoundsLoader
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader import ScaraBoundsLoader
from scarajectory.infrastructure.settings.bounds.scara_bounds_loader_factory import ScaraBoundsLoaderFactory
from scarajectory.infrastructure.settings.bounds.scara_bounds_parser_factory import ScaraBoundsParserFactory
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraBoundsLoader(TestCase):
    '''
        Unit test cases verifying ScaraBoundsLoader and factory.

        It defines:

            :methods:
                | setUp - Initializes loader fixture.
                | test_factory_interface - Verifies factory returns IScaraBoundsLoader protocol.
                | test_factory_create_with_reader - Verifies factory creation with explicit reader.
                | test_factory_version - Verifies factory version string.
                | test_load_bounds - Verifies bounds creation from JSON configuration.
                | test_load_bounds_with_options - Verifies override options in bounds creation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing ScaraBoundsLoader via factory.
        '''
        self.loader: IScaraBoundsLoader = ScaraBoundsLoaderFactory.create()

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs an instance satisfying IScaraBoundsLoader.
        '''
        self.assertIsInstance(self.loader, IScaraBoundsLoader)

    def test_factory_create_with_reader(self) -> None:
        '''
            Verifies factory constructs instance with explicit reader.
        '''
        loader: ScaraBoundsLoader = (
            ScaraBoundsLoaderFactory.create_with_reader(
                reader=SettingsReaderFactory.create()
            )
        )
        self.assertIsInstance(loader, IScaraBoundsLoader)

    def test_factory_create_with_collaborators(self) -> None:
        '''
            Verifies factory constructs instance with explicit reader and calculator.
        '''
        mock_calc = MagicMock()
        mock_calc.calculate_deadzone_radius.return_value = 42.0
        loader: ScaraBoundsLoader = (
            ScaraBoundsLoaderFactory.create_with_collaborators(
                reader=SettingsReaderFactory.create(),
                deadzone_calculator=mock_calc,
                parser=ScaraBoundsParserFactory.create(),
            )
        )
        self.assertIsInstance(loader, IScaraBoundsLoader)
        bounds: ScaraBounds = loader.load_bounds()
        self.assertEqual(bounds.deadzone_r_min, 42.0)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(ScaraBoundsLoaderFactory.get_version(), str)

    def test_load_bounds(self) -> None:
        '''
            Verifies load_bounds returns pure ScaraBounds populated from JSON SSoT.
        '''
        bounds: ScaraBounds = self.loader.load_bounds()
        self.assertIsInstance(bounds, ScaraBounds)
        self.assertEqual(bounds.l1, 150.0)
        self.assertEqual(bounds.l2, 120.0)
        self.assertEqual(bounds.z_min, 0.0)
        self.assertEqual(bounds.z_max, 100.0)
        self.assertEqual(bounds.default_speed, 50.0)
        self.assertGreater(bounds.deadzone_r_min, 0.0)

    def test_load_bounds_with_options(self) -> None:
        '''
            Verifies options override values from JSON configuration in bounds.
        '''
        bounds: ScaraBounds = self.loader.load_bounds_with_options(
            options={'l1': 160.0, 'l2': 130.0, 'default_speed': 60.0}
        )
        self.assertEqual(bounds.l1, 160.0)
        self.assertEqual(bounds.l2, 130.0)
        self.assertEqual(bounds.default_speed, 60.0)


if __name__ == '__main__':
    main()
