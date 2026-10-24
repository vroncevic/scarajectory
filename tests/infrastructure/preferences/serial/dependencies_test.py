# -*- coding: UTF-8 -*-

'''
Module
    dependencies_test.py
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
    Unit tests for SerialDependencies parameter dataclass.
'''

from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock

from scarajectory.infrastructure.preferences.serial.dependencies import SerialDependencies
from scarajectory.infrastructure.preferences.serial.repository import SerialPreferenceRepository
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


class SerialDependenciesTest(TestCase):
    '''Test cases verifying SerialDependencies structure and immutability.'''

    def test_dependencies_creation(self) -> None:
        '''Verifies SerialDependencies exposes config_loader, config_storer, and config_file.'''
        mock_loader = MagicMock(spec=IConfigLoader)
        mock_storer = MagicMock(spec=IConfigStorer)
        test_path = Path('/tmp/test_pref.json')
        deps = SerialDependencies(
            config_loader=mock_loader,
            config_storer=mock_storer,
            config_file=test_path,
        )
        self.assertIs(deps.config_loader, mock_loader)
        self.assertIs(deps.config_storer, mock_storer)
        self.assertEqual(deps.config_file, test_path)

    def test_dependencies_default_config_path(self) -> None:
        '''Verifies default configuration file path is SerialPreferenceRepository.DEFAULT_CONFIG_FILE.'''
        mock_loader = MagicMock(spec=IConfigLoader)
        mock_storer = MagicMock(spec=IConfigStorer)
        deps = SerialDependencies(
            config_loader=mock_loader,
            config_storer=mock_storer,
        )
        self.assertIs(deps.config_loader, mock_loader)
        self.assertIs(deps.config_storer, mock_storer)
        self.assertEqual(
            deps.config_file,
            SerialPreferenceRepository.DEFAULT_CONFIG_FILE,
        )

    def test_dependencies_immutability(self) -> None:
        '''Verifies SerialDependencies is frozen and rejects mutation.'''
        deps = SerialDependencies(
            config_loader=MagicMock(spec=IConfigLoader),
            config_storer=MagicMock(spec=IConfigStorer),
        )
        with self.assertRaises(FrozenInstanceError):
            deps.config_file = Path('/tmp/other.json')  # type: ignore[misc]


if __name__ == '__main__':
    main()
