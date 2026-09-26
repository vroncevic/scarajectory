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
    Infrastructure repository persisting and retrieving serial connection preferences using ats_utilities.
'''

from __future__ import annotations

from pathlib import Path
from typing import ClassVar

from ats_utilities.config_io.loader.engine import Loader
from ats_utilities.config_io.setup.factory import ConfigIOBundleFactory
from ats_utilities.config_io.setup.options import ConfigIOBundleOptions
from ats_utilities.config_io.storer.engine import Storer
from ats_utilities.context.bundle import ContextBundle
from ats_utilities.utils.reflection import to_str

from scarajectory.core.model.communication.preferences.connection_preference import ConnectionPreference
from scarajectory.core.service.communication.preferences.connection_preference_factory import ConnectionPreferenceFactory

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
        Repository managing file-based persistence for connection preferences using ats_utilities.

        It defines:

            :attributes:
                | DEFAULT_CONFIG_FILE - Default file path for storing connection preferences.
                | _config_file - Path to configuration storage file.
                | _context - ATS context bundle for configuration I/O operations.
            :methods:
                | __init__ - Initializes repository with injected ATS context bundle.
                | has_preference - Checks if saved preference configuration file exists on disk.
                | load_preference - Reads previously saved connection preference using ATS Loader.
                | save_preference - Persists active connection preference to storage using ATS Storer.
                | __str__ - Returns repository instance as string representation.
    '''

    DEFAULT_CONFIG_FILE: ClassVar[Path] = Path.home() / '.config' / 'scara' / 'serial_device.json'
    _config_file: Path
    _context: ContextBundle

    def __init__(self, context_bundle: ContextBundle) -> None:
        '''
            Initializes repository with injected ATS context bundle.

            :param context_bundle: ATS ContextBundle instance.
        '''
        self._config_file = self.DEFAULT_CONFIG_FILE
        self._context = context_bundle

    def has_preference(self) -> bool:
        '''
            Checks if saved preference configuration file exists on disk.

            :return: True if preference file exists, False otherwise.
        '''
        return self._config_file.is_file()

    def load_preference(self) -> ConnectionPreference:
        '''
            Reads previously saved connection preference using ATS Loader.

            :return: Loaded ConnectionPreference or default instance if not found.
        '''
        if not self.has_preference():
            return ConnectionPreferenceFactory.create_default()

        try:
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(file_path=str(self._config_file), context_bundle=self._context)
            )
            loader = Loader(bundle)
            payload: dict[str, object] = loader.load_configuration()
            raw_port = payload.get('port')
            raw_baud = payload.get('baud')

            if raw_port is None or raw_baud is None:
                return ConnectionPreferenceFactory.create_default()

            return ConnectionPreferenceFactory.create(port=str(raw_port), baud=int(raw_baud))

        except Exception:
            return ConnectionPreferenceFactory.create_default()

    def save_preference(self, preference: ConnectionPreference) -> bool:
        '''
            Persists active connection preference to storage using ATS Storer.

            :param preference: ConnectionPreference instance to persist.
            :return: True if persisted successfully, False otherwise.
        '''
        if not preference.port or preference.port == 'Virtual / None':
            return False

        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            self._config_file.touch(exist_ok=True)
            bundle = ConfigIOBundleFactory.create_bundle(
                ConfigIOBundleOptions(
                    file_path=str(self._config_file),
                    context_bundle=self._context
                )
            )
            storer = Storer(bundle)
            storer.store_configuration({'port': preference.port, 'baud': preference.baud})

            return True

        except Exception:
            return False

    def __str__(self) -> str:
        '''
            Returns the ConnectionRepository instance as string representation.

            :return: The ConnectionRepository instance as string representation.
        '''
        return to_str(self)
