# -*- coding: UTF-8 -*-

'''
Module
    scara_transmission_loader_test.py
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
    Unit tests for ScaraTransmissionLoader and ScaraTransmissionLoaderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main

from scaralang.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.settings.iscara_transmission_loader import IScaraTransmissionLoader
from scarajectory.infrastructure.settings.transmission.scara_transmission_loader import ScaraTransmissionLoader
from scarajectory.infrastructure.settings.transmission.scara_transmission_loader_factory import ScaraTransmissionLoaderFactory
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraTransmissionLoader(TestCase):
    '''
        Unit test cases verifying ScaraTransmissionLoader and factory.

        It defines:

            :methods:
                | setUp - Initializes loader fixture.
                | test_factory_interface - Verifies factory returns IScaraTransmissionLoader protocol.
                | test_factory_create_with_reader - Verifies factory creation with explicit reader.
                | test_factory_version - Verifies factory version string.
                | test_load_transmission - Verifies transmission creation from JSON configuration.
                | test_load_transmission_with_options - Verifies override options in transmission.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing ScaraTransmissionLoader via factory.
        '''
        self.loader: IScaraTransmissionLoader = (
            ScaraTransmissionLoaderFactory.create()
        )

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs an instance satisfying IScaraTransmissionLoader.
        '''
        self.assertIsInstance(self.loader, IScaraTransmissionLoader)

    def test_factory_create_with_reader(self) -> None:
        '''
            Verifies factory constructs instance with explicit reader.
        '''
        loader: ScaraTransmissionLoader = (
            ScaraTransmissionLoaderFactory.create_with_reader(
                reader=SettingsReaderFactory.create()
            )
        )
        self.assertIsInstance(loader, IScaraTransmissionLoader)

    def test_factory_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        self.assertIsInstance(ScaraTransmissionLoaderFactory.get_version(), str)

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
