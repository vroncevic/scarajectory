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
    Unit tests for BoundsFactory assembly.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.settings.bounds.dependencies import BoundsDependencies
from scarajectory.infrastructure.settings.bounds.factory import BoundsFactory
from scarajectory.infrastructure.settings.bounds.loader.iloader import IScaraBoundsLoader
from scarajectory.infrastructure.settings.bounds.parser.iparser import IScaraBoundsParser
from scarajectory.infrastructure.settings.bounds.provides import BoundsProvides
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


class TestBoundsFactory(TestCase):
    '''
        Test cases verifying BoundsFactory assembly.

        It defines:

            :methods:
                | test_create - Verifies factory creates BoundsProvides.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create(self) -> None:
        '''
            Verifies factory creates BoundsProvides with configured loader and parser.
        '''
        mock_loader: MagicMock = MagicMock(spec=IConfigLoader)
        reader_provides: ReaderProvides = ReaderFactory.create(
            ReaderDependencies(
                config_loader=mock_loader,
                config_path='/tmp/geo.json',
                scheme_path='/tmp/scheme.json',
            )
        )
        provides: BoundsProvides = BoundsFactory.create(
            BoundsDependencies(settings_reader=reader_provides.settings_reader)
        )
        self.assertIsInstance(provides, BoundsProvides)
        self.assertIsInstance(provides.bounds_loader, IScaraBoundsLoader)
        self.assertIsInstance(provides.bounds_parser, IScaraBoundsParser)

    def test_get_version(self) -> None:
        '''
            Verifies factory returns semantic version string.
        '''
        version = BoundsFactory.get_version()
        self.assertIsInstance(version, str)
        self.assertEqual(version, '1.0.3')


if __name__ == '__main__':
    main()
