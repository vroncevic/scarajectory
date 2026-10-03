# -*- coding: UTF-8 -*-

'''
Module
    connection_repository_test.py
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
    Unit tests for ConnectionRepository component.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from ats_utilities.context.factory import ContextBundleFactory

from scarajectory.core.model.preferences.connection_preference import (
    ConnectionPreference,
)
from scarajectory.core.service.preferences.iconnection_repository import (
    IConnectionRepository,
)
from scarajectory.infrastructure.preferences.connection_repository import (
    ConnectionRepository,
)

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionRepositoryTestCase(TestCase):
    '''
        Tests for ConnectionRepository persistence and error handling.

        It defines:

            :methods:
                | test_protocol_and_str - Tests structural protocol and string representation.
                | test_default_preference - Tests default preference when no file exists.
                | test_save_and_load_preference - Tests storing and reloading saved settings.
                | test_load_and_save_fallbacks - Tests error recovery during corrupted I/O.
    '''

    def test_protocol_and_str(self) -> None:
        '''Tests structural protocol conformance and string representation.'''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial.json'
            ctx = ContextBundleFactory.create_bundle()
            repo = ConnectionRepository(
                context_bundle=ctx,
                config_file=config_file,
            )
            self.assertIsInstance(repo, IConnectionRepository)
            self.assertIsInstance(str(repo), str)

    def test_default_preference(self) -> None:
        '''Tests default preference when no configuration file exists.'''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial.json'
            ctx = ContextBundleFactory.create_bundle()
            repo = ConnectionRepository(
                context_bundle=ctx,
                config_file=config_file,
            )
            self.assertFalse(repo.has_preference())
            pref = repo.load_preference()
            self.assertEqual(pref.port, ConnectionRepository.DEFAULT_PORT)
            self.assertEqual(pref.baud, ConnectionRepository.DEFAULT_BAUD)

    def test_save_and_load_preference(self) -> None:
        '''Tests storing and reloading valid and invalid settings.'''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial.json'
            ctx = ContextBundleFactory.create_bundle()
            repo = ConnectionRepository(
                context_bundle=ctx,
                config_file=config_file,
            )
            pref = ConnectionPreference(port='/dev/ttyUSB1', baud=57600)
            saved = repo.save_preference(pref)
            self.assertTrue(saved)
            self.assertTrue(repo.has_preference())

            loaded = repo.load_preference()
            self.assertEqual(loaded.port, '/dev/ttyUSB1')
            self.assertEqual(loaded.baud, 57600)

            empty_pref = ConnectionPreference(port='', baud=115200)
            self.assertFalse(repo.save_preference(empty_pref))

            virtual_pref = ConnectionPreference(
                port='Virtual / None', baud=9600
            )
            self.assertFalse(repo.save_preference(virtual_pref))

    @patch('scarajectory.infrastructure.preferences.connection_repository.Storer')
    @patch('scarajectory.infrastructure.preferences.connection_repository.Loader')
    def test_load_and_save_fallbacks(
        self, mock_loader_cls: MagicMock, mock_storer_cls: MagicMock
    ) -> None:
        '''Tests fallback to default preference on incomplete payload or exception.'''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial.json'
            config_file.touch()
            ctx = ContextBundleFactory.create_bundle()
            repo = ConnectionRepository(
                context_bundle=ctx,
                config_file=config_file,
            )

            mock_loader = MagicMock()
            mock_loader.load_configuration.return_value = {'other_key': 123}
            mock_loader_cls.return_value = mock_loader

            pref = repo.load_preference()
            self.assertEqual(pref.port, ConnectionRepository.DEFAULT_PORT)

            mock_loader.load_configuration.side_effect = RuntimeError('IO fail')
            pref_err = repo.load_preference()
            self.assertEqual(pref_err.port, ConnectionRepository.DEFAULT_PORT)

            mock_storer = MagicMock()
            mock_storer.store_configuration.side_effect = OSError('Disk full')
            mock_storer_cls.return_value = mock_storer

            valid_pref = ConnectionPreference(
                port='/dev/ttyUSB0', baud=115200
            )
            self.assertFalse(repo.save_preference(valid_pref))


if __name__ == '__main__':
    main()
