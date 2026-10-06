# -*- coding: UTF-8 -*-

'''
Module
    config_io_factory_test.py
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
    Unit testing for ConfigIOFactory component.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from unittest import TestCase, main

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

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


class ConfigIOFactoryTestCase(TestCase):
    '''Unit tests validating ConfigIOFactory behavior and protocol conformance.'''

    def setUp(self) -> None:
        '''Initializes shared test fixtures.'''
        self.context: ContextBundle = ContextBundleFactory.create_bundle()
        self.factory: ConfigIOFactory = ConfigIOFactory.create(self.context)

    def test_protocol_conformance(self) -> None:
        '''Verifies ConfigIOFactory satisfies IConfigIOFactory protocol.'''
        self.assertIsInstance(self.factory, IConfigIOFactory)

    def test_create_loader(self) -> None:
        '''Verifies create_loader returns configured Loader instance.'''
        with NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp.write(b'{"key": "value"}')
            tmp_path: str = tmp.name

        try:
            loader = self.factory.create_loader(tmp_path)
            self.assertIsInstance(loader, Loader)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_create_storer(self) -> None:
        '''Verifies create_storer returns configured Storer instance.'''
        with NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp_path: str = tmp.name

        try:
            storer = self.factory.create_storer(tmp_path)
            self.assertIsInstance(storer, Storer)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_create_validated_loader_without_scheme(self) -> None:
        '''Verifies create_validated_loader succeeds when scheme file does not exist.'''
        with NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp.write(b'{"key": "value"}')
            tmp_path: str = tmp.name

        try:
            loader = self.factory.create_validated_loader(
                tmp_path, '/nonexistent/scheme.json'
            )
            self.assertIsInstance(loader, Loader)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_get_version(self) -> None:
        '''Verifies get_version returns semantic version string.'''
        self.assertEqual(ConfigIOFactory.get_version(), '1.0.3')


if __name__ == '__main__':
    main()
