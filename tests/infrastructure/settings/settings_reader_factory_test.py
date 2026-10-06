# -*- coding: UTF-8 -*-

'''
Module
    settings_reader_factory_test.py
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
    Unit tests for SettingsReaderFactory instantiation and assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.settings.settings_reader import SettingsReader
from scarajectory.infrastructure.settings.settings_reader_factory import SettingsReaderFactory
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


class TestSettingsReaderFactory(TestCase):
    '''
        Test cases verifying SettingsReaderFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory creates SettingsReader with default configuration.
                | test_create_with_context - Verifies assembly with explicit ContextBundle.
                | test_create_with_paths - Verifies assembly with explicit file paths.
                | test_create_with_io_factory - Verifies assembly with explicit IConfigIOFactory.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid SettingsReader instance with defaults.
        '''
        reader = SettingsReaderFactory.create()
        self.assertIsInstance(reader, SettingsReader)

    def test_create_with_context(self) -> None:
        '''
            Verifies factory creates SettingsReader with explicit ContextBundle.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        reader = SettingsReaderFactory.create_with_context(context_bundle=bundle)
        self.assertIsInstance(reader, SettingsReader)

    def test_create_with_paths(self) -> None:
        '''
            Verifies factory creates SettingsReader with explicit configuration paths.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        reader = SettingsReaderFactory.create_with_paths(
            config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
            scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            context_bundle=bundle,
        )
        self.assertIsInstance(reader, SettingsReader)

    def test_create_with_io_factory(self) -> None:
        '''
            Verifies factory creates SettingsReader with explicit IConfigIOFactory.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_factory: IConfigIOFactory = ConfigIOFactory.create(bundle)
        reader = SettingsReaderFactory.create_with_io_factory(
            config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
            scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            io_factory=io_factory,
        )
        self.assertIsInstance(reader, SettingsReader)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string.
        '''
        version = SettingsReaderFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
