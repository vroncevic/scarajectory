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
    Unit tests for BoundsLoaderFactory.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.settings.bounds.loader.dependencies import LoaderDependencies
from scarajectory.infrastructure.settings.bounds.loader.factory import BoundsLoaderFactory
from scarajectory.infrastructure.settings.bounds.loader.iloader import IScaraBoundsLoader
from scarajectory.infrastructure.settings.bounds.loader.provides import LoaderProvides
from scarajectory.infrastructure.settings.bounds.parser.parser import ScaraBoundsParser
from scarajectory.infrastructure.settings.reader.dependencies import ReaderDependencies
from scarajectory.infrastructure.settings.reader.factory import ReaderFactory
from scarajectory.infrastructure.settings.reader.provides import ReaderProvides
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TestBoundsLoaderFactory(TestCase):
    '''
        Unit test cases verifying BoundsLoaderFactory operations.

        It defines:

            :methods:
                | test_create - Verifies factory creates loader wrapped in LoaderProvides.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates loader wrapped in LoaderProvides.
        '''
        mock_loader: MagicMock = MagicMock(spec=IConfigLoader)
        reader_provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=mock_loader,
                config_path='/tmp/geo.json',
                scheme_path='/tmp/scheme.json',
            )
        )
        provides: LoaderProvides = BoundsLoaderFactory.create(
            LoaderDependencies(
                settings_reader=reader_provides.settings_reader,
                bounds_parser=ScaraBoundsParser(),
            )
        )
        self.assertIsInstance(provides, LoaderProvides)
        self.assertIsInstance(provides.bounds_loader, IScaraBoundsLoader)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns version string.
        '''
        version = BoundsLoaderFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
