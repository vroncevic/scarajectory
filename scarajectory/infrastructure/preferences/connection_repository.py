# -*- coding: UTF-8 -*-

'''
Module
    connection_repository.py
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
    Infrastructure repository persisting and retrieving serial connection preferences.
'''

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from ats_utilities.utils.reflection import to_str

from scarajectory.core.model.preferences.connection_preference import ConnectionPreference
from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_loader import IConfigLoader
from scarajectory.infrastructure.storage.config_io.iconfig_storer import IConfigStorer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConnectionRepository:
    '''
        Repository managing file-based persistence for connection preferences.

        It defines:

            :attributes:
                | DEFAULT_CONFIG_FILE - Default file path for storing connection preferences.
                | DEFAULT_PORT - Default serial port string identifier.
                | DEFAULT_BAUD - Default serial baud rate frequency integer.
                | _config_file - Path to configuration storage file.
                | _io_factory - Configuration I/O factory constructing loaders and storers.
            :methods:
                | __init__ - Initializes repository with injected I/O factory and config file.
                | has_preference - Checks if saved preference configuration file exists on disk.
                | load_preference - Reads previously saved connection preference using loader.
                | save_preference - Persists active connection preference to storage using storer.
                | __str__ - Returns repository instance as string representation.
    '''

    DEFAULT_CONFIG_FILE: ClassVar[Path] = (
        Path.home() / '.config' / 'scara' / 'serial_device.json'
    )
    DEFAULT_PORT: ClassVar[str] = '/dev/ttyACM0'
    DEFAULT_BAUD: ClassVar[int] = 115200

    _config_file: Path
    _io_factory: IConfigIOFactory

    def __init__(
        self,
        *,
        io_factory: IConfigIOFactory,
        config_file: Path,
    ) -> None:
        '''
            Initializes repository with injected configuration I/O factory and config path.

            :param io_factory: IConfigIOFactory instance.
            :param config_file: Path to configuration storage file.
        '''
        self._config_file = config_file
        self._io_factory = io_factory

    def has_preference(self) -> bool:
        '''
            Checks if saved preference configuration file exists on disk.

            :return: True if preference file exists, False otherwise.
        '''
        return self._config_file.is_file()

    def load_preference(self) -> ConnectionPreference:
        '''
            Reads previously saved connection preference using configuration loader.

            :return: Loaded ConnectionPreference or default instance if not found.
        '''
        if not self.has_preference():
            return ConnectionPreference(
                port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
            )

        try:
            loader: IConfigLoader = self._io_factory.create_loader(
                str(self._config_file)
            )
            payload: dict[str, object] = loader.load_configuration()
            if ('port' not in payload) or ('baud' not in payload):
                return ConnectionPreference(
                    port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
                )

            raw_port: str = str(payload['port'])
            raw_baud: int = int(payload['baud'])
            return ConnectionPreference(port=raw_port, baud=raw_baud)

        except Exception:
            return ConnectionPreference(
                port=self.DEFAULT_PORT, baud=self.DEFAULT_BAUD
            )

    def save_preference(self, preference: ConnectionPreference) -> bool:
        '''
            Persists active connection preference to storage using configuration storer.

            :param preference: ConnectionPreference instance to persist.
            :return: True if persisted successfully, False otherwise.
        '''
        if not preference.port or preference.port == 'Virtual / None':
            return False

        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.touch(exist_ok=True)
            storer: IConfigStorer = self._io_factory.create_storer(
                str(self._config_file)
            )
            storer.store_configuration(
                {'port': preference.port, 'baud': preference.baud}
            )
            return True

        except Exception:
            return False

    def __str__(self) -> str:
        '''
            Returns the ConnectionRepository instance as string representation.

            :return: The ConnectionRepository instance as string representation.
        '''
        return to_str(self)
