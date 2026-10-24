# -*- coding: UTF-8 -*-

'''
Module
    repository_test.py
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
    Unit tests for SerialPreferenceRepository component.
'''

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase, main
from unittest.mock import MagicMock

from ats_utilities.context.bundle import ContextBundle
from ats_utilities.context.factory import ContextBundleFactory

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.preference.preference import SerialPreference
from scarajectory.infrastructure.preferences.serial.repository import SerialPreferenceRepository
from scarajectory.infrastructure.storage.config_io.dependencies import ConfigIODependencies
from scarajectory.infrastructure.storage.config_io.factory import ConfigIOFactory
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.storer.istorer import IConfigStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SerialPreferenceRepositoryTestCase(TestCase):
    '''Tests for SerialPreferenceRepository persistence, fallback, and error handling.'''

    def setUp(self) -> None:
        '''
            Sets up test fixtures before each test method.

            :exceptions: None.
        '''
        self.context: ContextBundle = ContextBundleFactory.create_bundle()
        io_provides = ConfigIOFactory.create(
            ConfigIODependencies(context_bundle=self.context)
        )
        self.loader: IConfigLoader = io_provides.config_loader
        self.storer: IConfigStorer = io_provides.config_storer

    def test_repository_satisfies_protocol(self) -> None:
        '''
            Verifies SerialPreferenceRepository structurally satisfies ISerialPreferenceRepository.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_preferences.json'
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=self.storer, config_file=config_file
            )
            self.assertIsInstance(repo, ISerialPreferenceRepository)

    def test_load_preference_default_when_missing(self) -> None:
        '''
            Verifies load_preference returns default values when no file exists.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'nonexistent.json'
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=self.storer, config_file=config_file
            )
            self.assertFalse(repo.has_preference())
            pref = repo.load_preference()
            self.assertEqual(pref.port, SerialPreferenceRepository.DEFAULT_PORT)
            self.assertEqual(pref.baud, SerialPreferenceRepository.DEFAULT_BAUD)

    def test_save_and_load_preference_roundtrip(self) -> None:
        '''
            Verifies save_preference successfully persists data and load_preference retrieves it.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_preferences.json'
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=self.storer, config_file=config_file
            )

            pref_to_save = SerialPreference(port='/dev/ttyUSB1', baud=57600)
            success = repo.save_preference(pref_to_save)
            self.assertTrue(success)
            self.assertTrue(repo.has_preference())

            loaded = repo.load_preference()
            self.assertEqual(loaded.port, '/dev/ttyUSB1')
            self.assertEqual(loaded.baud, 57600)

    def test_save_preference_invalid_port_rejected(self) -> None:
        '''
            Verifies empty port or virtual none port is rejected by save_preference.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_preferences.json'
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=self.storer, config_file=config_file
            )
            self.assertFalse(
                repo.save_preference(SerialPreference(port='', baud=115200))
            )
            self.assertFalse(
                repo.save_preference(
                    SerialPreference(port='Virtual / None', baud=115200)
                )
            )

    def test_load_preference_corrupted_or_missing_keys_fallback(self) -> None:
        '''
            Verifies fallback to default if payload has missing keys or exception occurs.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'bad_config.json'
            config_file.write_text('{"other_key": 123}', encoding='utf-8')
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=self.storer, config_file=config_file
            )
            self.assertTrue(repo.has_preference())
            pref = repo.load_preference()
            self.assertEqual(pref.port, SerialPreferenceRepository.DEFAULT_PORT)

            config_file.write_text('["not_a_dict"]', encoding='utf-8')
            pref_list = repo.load_preference()
            self.assertEqual(pref_list.port, SerialPreferenceRepository.DEFAULT_PORT)

            mock_loader = MagicMock()
            mock_loader.load.side_effect = RuntimeError('Disk read error')
            repo_err = SerialPreferenceRepository(
                loader=mock_loader, storer=self.storer, config_file=config_file
            )
            pref_err = repo_err.load_preference()
            self.assertEqual(pref_err.port, SerialPreferenceRepository.DEFAULT_PORT)

    def test_save_preference_io_exception_returns_false(self) -> None:
        '''
            Verifies save_preference returns False if storer raises an exception.

            :exceptions: None.
        '''
        mock_storer = MagicMock(spec=IConfigStorer)
        mock_storer.store.side_effect = RuntimeError('Disk full')
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_preferences.json'
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=mock_storer, config_file=config_file
            )
            success = repo.save_preference(
                SerialPreference(port='/dev/ttyACM0', baud=115200)
            )
            self.assertFalse(success)

    def test_version_and_str(self) -> None:
        '''
            Verifies get_version and string representation.

            :exceptions: None.
        '''
        with TemporaryDirectory() as tmp_dir:
            config_file = Path(tmp_dir) / 'serial_preferences.json'
            repo = SerialPreferenceRepository(
                loader=self.loader, storer=self.storer, config_file=config_file
            )
            self.assertEqual(repo.get_version(), '1.0.3')
            self.assertIn('SerialPreferenceRepository', str(repo))


if __name__ == '__main__':
    main()
