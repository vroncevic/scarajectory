# -*- coding: UTF-8 -*-

'''
Module
    settings_reader_test.py
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
    Unit tests for SettingsReader configuration loading and queries.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.settings.settings_reader import SettingsReader
from scarajectory.infrastructure.storage.config_io.config_io_factory import ConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestSettingsReader(TestCase):
    '''
        Unit test cases verifying SettingsReader file reading and query operations.

        It defines:

            :methods:
                | setUp - Initializes reader fixture.
                | test_read_settings - Verifies loading raw dictionary from JSON configuration.
                | test_get_setting - Verifies reading individual setting with fallback.
    '''

    reader: SettingsReader

    def setUp(self) -> None:
        '''
            Sets up test fixture initializing SettingsReader with default config paths.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_factory: IConfigIOFactory = ConfigIOFactory.create(bundle)
        self.reader = SettingsReader(
            config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
            scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            io_factory=io_factory,
        )

    def test_read_settings(self) -> None:
        '''
            Verifies read_settings returns dictionary with expected keys.
        '''
        raw: dict[str, float] = self.reader.read_settings()
        self.assertIsInstance(raw, dict)
        self.assertIn('l1', raw)
        self.assertIn('l2', raw)
        self.assertIn('steps_per_rev', raw)
        self.assertEqual(raw['l1'], 150.0)
        self.assertEqual(raw['l2'], 120.0)

        missing_reader = SettingsReader(
            config_path='/tmp/missing_scarajectory_config.json',
            scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            io_factory=self.reader._io_factory,  # pylint: disable=protected-access
        )
        self.assertEqual(missing_reader.read_settings(), {})

    def test_get_setting(self) -> None:
        '''
            Verifies get_setting resolves existing and fallback keys.
        '''
        val: float = self.reader.get_setting(key='l1', default_val=100.0)
        self.assertEqual(val, 150.0)
        fallback: float = self.reader.get_setting(
            key='non_existent_key', default_val=42.0
        )
        self.assertEqual(fallback, 42.0)


if __name__ == '__main__':
    main()
