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
    Unit tests for ReaderFactory instantiation and assembly.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

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


class TestReaderFactory(TestCase):
    '''
        Test cases verifying ReaderFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory creates SettingsReader wrapped in ReaderProvides.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates a valid SettingsReader instance wrapped in ReaderProvides.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=bundle)
        )
        provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=io_provides.config_loader,
                config_path='/tmp/geometry.json',
                scheme_path='/tmp/schema.json',
            )
        )
        self.assertIsInstance(provides, ReaderProvides)
        self.assertIsInstance(provides.settings_reader, SettingsReader)

    def test_create_default(self) -> None:
        '''
            Verifies factory creates SettingsReader with default path dependencies.
        '''
        bundle: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=bundle)
        )
        provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        self.assertIsInstance(provides, ReaderProvides)
        self.assertIsInstance(provides.settings_reader, SettingsReader)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string.
        '''
        version = ReaderFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
