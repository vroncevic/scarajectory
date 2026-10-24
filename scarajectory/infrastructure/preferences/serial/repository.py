# -*- coding: UTF-8 -*-

'''
Module
    repository.py
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
    Repository managing file-based persistence for serial connection preferences.
'''

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from ats_utilities.utils.reflection import to_str
from scaracom.transport.preference.preference import SerialPreference

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


class SerialPreferenceRepository:
    '''
        Repository managing file-based persistence for serial connection preferences.

        It defines:

            :attributes:
                | DEFAULT_CONFIG_FILE - Default file path for storing serial preferences.
                | LEGACY_CONFIG_FILE - Legacy file path for backward-compatible fallback.
                | DEFAULT_PORT - Default serial port string identifier.
                | DEFAULT_BAUD - Default serial baud rate frequency integer.
                | _config_file - Path to configuration storage file.
                | _loader - Injected IConfigLoader protocol collaborator.
                | _storer - Injected IConfigStorer protocol collaborator.

            :methods:
                | __init__ - Initializes repository with injected loader, storer, and config file.
                | has_preference - Checks if saved preference configuration file exists on disk.
                | load_preference - Reads previously saved serial connection preference using loader.
                | save_preference - Persists active serial connection preference to storage using storer.
                | get_version - Returns repository semantic version string.
                | __str__ - Returns repository instance as string representation.
    '''

    DEFAULT_CONFIG_FILE: ClassVar[Path] = (
        Path.home() / '.config' / 'scara' / 'serial_preferences.json'
    )
    LEGACY_CONFIG_FILE: ClassVar[Path] = (
        Path.home() / '.config' / 'scara' / 'serial_device.json'
    )
    DEFAULT_PORT: ClassVar[str] = '/dev/ttyACM0'
    DEFAULT_BAUD: ClassVar[int] = 115200

    _config_file: Path
    _loader: IConfigLoader
    _storer: IConfigStorer

    def __init__(
        self,
        *,
        loader: IConfigLoader,
        storer: IConfigStorer,
        config_file: Path,
    ) -> None:
        '''
            Initializes repository with injected loader, storer, and config path.

            :param loader: Injected IConfigLoader instance.
            :param storer: Injected IConfigStorer instance.
            :param config_file: Path to configuration storage file.
        '''
        self._config_file = config_file
        self._loader = loader
        self._storer = storer

    def has_preference(self) -> bool:
        '''
            Checks if saved preference configuration file exists on disk.

            :return: True if preference file exists, False otherwise.
        '''
        return self._config_file.is_file() or (
            self._config_file == self.DEFAULT_CONFIG_FILE
            and self.LEGACY_CONFIG_FILE.is_file()
        )

    def load_preference(self) -> SerialPreference:
        '''
            Reads previously saved serial connection preference using configuration loader.

            :return: Loaded SerialPreference or default instance if not found.
        '''
        if not self.has_preference():
            return SerialPreference(
                port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
            )

        target_file: Path = (
            self._config_file
            if self._config_file.is_file()
            else self.LEGACY_CONFIG_FILE
        )

        try:
            payload: object = self._loader.load(str(target_file))
            if not isinstance(payload, dict):
                return SerialPreference(
                    port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
                )
            if ('port' not in payload) or ('baud' not in payload):
                return SerialPreference(
                    port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
                )

            raw_port: str = str(payload['port'])
            raw_baud: int = int(payload['baud'])
            return SerialPreference(port=raw_port, baud=raw_baud)

        except Exception:
            return SerialPreference(
                port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
            )

    def save_preference(self, preference: SerialPreference) -> bool:
        '''
            Persists active serial connection preference to storage using configuration storer.

            :param preference: SerialPreference instance to persist.
            :return: True if persisted successfully, False otherwise.
        '''
        if not preference.port or preference.port == 'Virtual / None':
            return False

        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.touch(exist_ok=True)
            self._storer.store(
                str(self._config_file),
                {'port': preference.port, 'baud': preference.baud}
            )
            return True

        except Exception:
            return False

    def get_version(self) -> str:
        '''
            Returns repository module semantic version string.

            :return: Semantic version string (__version__).
            :exceptions: None.
        '''
        return __version__

    def __str__(self) -> str:
        '''
            Returns formatted string representation of repository state.

            :return: Formatted string representing repository properties.
        '''
        return to_str(self)
