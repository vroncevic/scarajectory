# -*- coding: UTF-8 -*-

'''
Module
    ireader_test.py
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
    Unit testing for ISettingsReader protocol conformance.
'''

from __future__ import annotations

from unittest import TestCase, main

from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.settings.reader.dependencies import ReaderDependencies
from scarajectory.infrastructure.settings.reader.factory import ReaderFactory
from scarajectory.infrastructure.settings.reader.ireader import ISettingsReader
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


class ConformingSettingsReaderStub:
    '''Conforming stub implementation satisfying ISettingsReader protocol.'''

    def read_settings(self) -> dict[str, float]:
        '''Reads settings dictionary.'''
        return {'l1': 150.0}

    def get_setting(self, *, key: str, default_val: float) -> float:
        '''Gets setting by key.'''
        _ = key
        return default_val


class IncompleteSettingsReaderStub:
    '''Non-conforming stub implementation missing get_setting.'''

    def read_settings(self) -> dict[str, float]:
        '''Reads settings dictionary.'''
        return {}

    def other_action(self) -> None:
        '''Dummy method to satisfy method count.'''


class SettingsReaderProtocolTestCase(TestCase):
    '''
        Tests ISettingsReader runtime checkable protocol conformance.

        It defines:

            :methods:
                | test_protocol_conformance_success - Verifies conforming class passes check.
                | test_protocol_conformance_failure - Verifies non-conforming class fails check.
                | test_settings_reader_conformance - Verifies concrete SettingsReader satisfies it.
    '''

    def test_protocol_conformance_success(self) -> None:
        '''Verifies compliant class satisfies ISettingsReader protocol.'''
        stub = ConformingSettingsReaderStub()
        self.assertIsInstance(stub, ISettingsReader)

    def test_protocol_conformance_failure(self) -> None:
        '''Verifies non-compliant class fails ISettingsReader protocol check.'''
        stub = IncompleteSettingsReaderStub()
        self.assertNotIsInstance(stub, ISettingsReader)

    def test_settings_reader_conformance(self) -> None:
        '''Verifies concrete SettingsReader structurally satisfies ISettingsReader.'''
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=ContextBundleFactory.create_bundle())
        )
        provides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=io_provides.config_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        self.assertIsInstance(provides.settings_reader, ISettingsReader)


if __name__ == '__main__':
    main()
