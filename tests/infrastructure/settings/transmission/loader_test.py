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
    Unit tests for ScaraTransmissionLoader.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory
from scaralang.core.model.kinematics.profile.transmission import TransmissionParameters

from scarajectory.infrastructure.settings.reader.dependencies import ReaderDependencies
from scarajectory.infrastructure.settings.reader.factory import ReaderFactory
from scarajectory.infrastructure.settings.reader.provides import ReaderProvides
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.settings.transmission.loader import ScaraTransmissionLoader
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


class TestScaraTransmissionLoader(TestCase):
    '''
        Unit test cases verifying ScaraTransmissionLoader operations.

        It defines:

            :methods:
                | setUp - Initializes loader fixture.
                | test_load_transmission - Verifies transmission creation from JSON configuration.
                | test_load_transmission_with_options - Verifies override options in transmission.
    '''

    loader: ScaraTransmissionLoader

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing ScaraTransmissionLoader.
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
        self.loader = ScaraTransmissionLoader(
            settings_reader=reader_provides.settings_reader
        )

    def test_load_transmission(self) -> None:
        '''
            Verifies load_transmission returns pure TransmissionParameters from JSON.
        '''
        transmission: TransmissionParameters = self.loader.load_transmission()
        self.assertIsInstance(transmission, TransmissionParameters)
        self.assertEqual(transmission.steps_per_rev, 200.0)
        self.assertEqual(transmission.microstepping, 16.0)
        self.assertEqual(transmission.gear_ratio_j1, 4.0)
        self.assertEqual(transmission.gear_ratio_j2, 4.0)
        self.assertEqual(transmission.gear_ratio_j4, 1.0)
        self.assertEqual(transmission.leadscrew_pitch_z, 8.0)

    def test_load_transmission_with_options(self) -> None:
        '''
            Verifies options override values from JSON in transmission model.
        '''
        transmission: TransmissionParameters = (
            self.loader.load_transmission_with_options(
                options={'microstepping': 32.0, 'steps_per_rev': 400.0}
            )
        )
        self.assertEqual(transmission.microstepping, 32.0)
        self.assertEqual(transmission.steps_per_rev, 400.0)


if __name__ == '__main__':
    main()
