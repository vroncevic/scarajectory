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
    Unit tests for TransmissionFactory assembly.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.settings.reader.dependencies import ReaderDependencies
from scarajectory.infrastructure.settings.reader.factory import ReaderFactory
from scarajectory.infrastructure.settings.reader.provides import ReaderProvides
from scarajectory.infrastructure.settings.reader.reader import SettingsReader
from scarajectory.infrastructure.settings.transmission.dependencies import TransmissionDependencies
from scarajectory.infrastructure.settings.transmission.factory import TransmissionFactory
from scarajectory.infrastructure.settings.transmission.iloader import IScaraTransmissionLoader
from scarajectory.infrastructure.settings.transmission.provides import TransmissionProvides
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestTransmissionFactory(TestCase):
    '''
        Test cases verifying TransmissionFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory creates loader wrapped in TransmissionProvides.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates loader wrapped in TransmissionProvides.
        '''
        mock_loader: MagicMock = MagicMock(spec=IConfigLoader)
        reader_provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=mock_loader,
                config_path=SettingsReader.DEFAULT_GEOMETRY_CONFIG,
                scheme_path=SettingsReader.DEFAULT_SCHEME_CONFIG,
            )
        )
        provides: TransmissionProvides = TransmissionFactory.create(
            TransmissionDependencies(settings_reader=reader_provides.settings_reader)
        )
        self.assertIsInstance(provides, TransmissionProvides)
        self.assertIsInstance(provides.transmission_loader, IScaraTransmissionLoader)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string.
        '''
        version = TransmissionFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
