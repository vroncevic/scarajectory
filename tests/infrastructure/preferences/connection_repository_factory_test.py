# -*- coding: UTF-8 -*-

'''
Module
    connection_repository_factory_test.py
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
    Unit testing for ConnectionRepositoryFactory component.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main

from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.infrastructure.preferences.connection_repository import ConnectionRepository
from scarajectory.infrastructure.preferences.connection_repository_factory import ConnectionRepositoryFactory
from scarajectory.infrastructure.storage.config_io.config_io_factory import ConfigIOFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionRepositoryFactoryTestCase(TestCase):
    '''
        Unit tests for ConnectionRepositoryFactory.

        It defines:

            :methods:
                | test_create_default - Verifies factory creates repository with default path.
                | test_create_with_path - Verifies factory creates repository with custom path.
                | test_create_with_io_factory - Verifies factory creates repository with IConfigIOFactory.
                | test_get_version - Verifies factory returns semantic version string.
    '''

    def test_create_default(self) -> None:
        '''Verifies factory creates repository with default configuration path.'''
        ctx = ContextBundleFactory.create_bundle()
        repo = ConnectionRepositoryFactory.create(ctx)
        self.assertIsInstance(repo, ConnectionRepository)

    def test_create_with_path(self) -> None:
        '''Verifies factory creates repository with specified custom path.'''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'custom_pref.json'
            ctx = ContextBundleFactory.create_bundle()
            repo = ConnectionRepositoryFactory.create_with_path(
                context_bundle=ctx,
                config_file=config_file,
            )
            self.assertIsInstance(repo, ConnectionRepository)

    def test_create_with_io_factory(self) -> None:
        '''Verifies factory creates repository with injected IConfigIOFactory.'''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'custom_pref.json'
            ctx = ContextBundleFactory.create_bundle()
            io_factory = ConfigIOFactory.create(ctx)
            repo = ConnectionRepositoryFactory.create_with_io_factory(
                io_factory=io_factory,
                config_file=config_file,
            )
            self.assertIsInstance(repo, ConnectionRepository)

    def test_get_version(self) -> None:
        '''Verifies factory exposes semantic version string matching package.'''
        self.assertEqual(
            ConnectionRepositoryFactory.get_version(), '1.0.3'
        )


if __name__ == '__main__':
    main()
