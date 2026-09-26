# -*- coding: UTF-8 -*-

'''
Module
    scara_config_loader_test.py
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
    Unit tests for ScaraConfigLoader and ScaraConfigLoaderFactory.
'''

from __future__ import annotations

from os.path import abspath, dirname
from sys import path
from unittest import TestCase, main

pkg_dir: str = dirname(dirname(abspath(__file__)))
if pkg_dir not in path:
    path.insert(0, pkg_dir)

from scarajectory.core.model.communication.stream.stream_config import StreamConfig
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters
from scarajectory.core.service.config.iscara_config_loader import IScaraConfigLoader
from scarajectory.infrastructure.settings.config_loader_factory import ScaraConfigLoaderFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestScaraConfigLoader(TestCase):
    '''
        Unit test cases verifying ScaraConfigLoader and factory.

        It defines:

            :methods:
                | setUp - Initializes loader fixture.
                | test_factory_interface - Verifies factory returns IScaraConfigLoader protocol.
                | test_load_raw_config - Verifies loading raw dictionary from JSON configuration.
                | test_load_bounds - Verifies bounds creation from JSON configuration.
                | test_load_bounds_with_options - Verifies override options precedence in bounds creation.
                | test_load_transmission - Verifies transmission creation from JSON configuration.
                | test_load_transmission_with_options - Verifies override options in transmission creation.
    '''

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing IScaraConfigLoader via factory.
        '''
        self.loader: IScaraConfigLoader = ScaraConfigLoaderFactory.create()

    def test_factory_interface(self) -> None:
        '''
            Verifies factory constructs an instance satisfying IScaraConfigLoader.
        '''
        self.assertIsInstance(self.loader, IScaraConfigLoader)

    def test_load_raw_config(self) -> None:
        '''
            Verifies load_raw_config returns dictionary with expected keys.
        '''
        raw: dict[str, float] = self.loader.load_raw_config()
        self.assertIsInstance(raw, dict)
        self.assertIn('l1', raw)
        self.assertIn('l2', raw)
        self.assertIn('steps_per_rev', raw)
        self.assertIn('microstepping', raw)
        self.assertIn('gear_ratio_j1', raw)
        self.assertEqual(raw['l1'], 150.0)
        self.assertEqual(raw['l2'], 120.0)

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
        transmission: TransmissionParameters = self.loader.load_transmission_with_options(
            options={'microstepping': 32.0, 'steps_per_rev': 400.0}
        )
        self.assertEqual(transmission.microstepping, 32.0)
        self.assertEqual(transmission.steps_per_rev, 400.0)

    def test_load_stream_config(self) -> None:
        '''
            Verifies load_stream_config returns pure StreamConfig from JSON SSoT.
        '''
        config: StreamConfig = self.loader.load_stream_config(port='/dev/ttyUSB0')
        self.assertIsInstance(config, StreamConfig)
        self.assertEqual(config.port, '/dev/ttyUSB0')
        self.assertEqual(config.baudrate, 115200)
        self.assertAlmostEqual(config.timeout, 0.1)

    def test_load_stream_config_with_options(self) -> None:
        '''
            Verifies options override values from JSON in stream config model.
        '''
        config: StreamConfig = self.loader.load_stream_config_with_options(
            port='COM5',
            options={'baudrate': 9600.0, 'timeout': 1.5}
        )
        self.assertEqual(config.port, 'COM5')
        self.assertEqual(config.baudrate, 9600)
        self.assertAlmostEqual(config.timeout, 1.5)


if __name__ == '__main__':
    main()
