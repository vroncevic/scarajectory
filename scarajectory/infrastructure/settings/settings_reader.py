# -*- coding: UTF-8 -*-

'''
Module
    settings_reader.py
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
    Infrastructure reader for caching raw SCARA JSON configuration settings.
'''

from __future__ import annotations

from os.path import abspath, dirname, exists, join
from typing import ClassVar

from scarajectory.infrastructure.storage.config_io.iconfig_io_factory import IConfigIOFactory
from scarajectory.infrastructure.storage.config_io.iconfig_loader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SettingsReader:
    '''
        Reader adapter caching raw robot settings from JSON schema and config files.

        It defines:

            :attributes:
                | DEFAULT_GEOMETRY_CONFIG - Default absolute path to scara_geometry.json.
                | DEFAULT_SCHEME_CONFIG - Default absolute path to scheme.json.
                | _config_path - Absolute path to scara_geometry.json.
                | _scheme_path - Absolute path to scheme.json.
                | _io_factory - The configuration I/O factory constructing loaders.
                | _cached_config - Cached raw configuration dictionary.

            :methods:
                | __init__ - Initializes SettingsReader with configuration file paths and I/O factory.
                | read_settings - Loads and caches raw dictionary of settings.
                | get_setting - Retrieves setting value by key with required fallback value.
    '''

    DEFAULT_GEOMETRY_CONFIG: ClassVar[str] = join(
        dirname(dirname(abspath(__file__))), 'config', 'scara_geometry.json'
    )
    DEFAULT_SCHEME_CONFIG: ClassVar[str] = join(
        dirname(dirname(abspath(__file__))), 'config', 'scheme.json'
    )

    _config_path: str
    _scheme_path: str
    _io_factory: IConfigIOFactory
    _cached_config: dict[str, float]

    def __init__(
        self,
        *,
        config_path: str,
        scheme_path: str,
        io_factory: IConfigIOFactory,
    ) -> None:
        '''
            Initializes SettingsReader with configuration file paths and I/O factory.

            :param config_path: Absolute path to geometry configuration file.
            :param scheme_path: Absolute path to validation schema file.
            :param io_factory: Injected IConfigIOFactory instance.
        '''
        self._config_path = config_path
        self._scheme_path = scheme_path
        self._io_factory = io_factory
        self._cached_config = {}

    def read_settings(self) -> dict[str, float]:
        '''
            Reads and returns configuration parameters dictionary using configuration loader.

            :return: Dictionary of configuration keys to float values.
        '''
        if self._cached_config:
            return self._cached_config

        if not exists(self._config_path):
            return {}

        loader: IConfigLoader = self._io_factory.create_validated_loader(
            filepath=self._config_path,
            scheme_path=self._scheme_path,
        )
        data: object = loader.load_configuration()

        if isinstance(data, dict):
            self._cached_config = {
                str(k): float(v)
                for k, v in data.items()
                if isinstance(v, (int, float))
            }

        return self._cached_config

    def get_setting(self, *, key: str, default_val: float) -> float:
        '''
            Retrieves setting value by key with required fallback value.

            :param key: Configuration setting name.
            :param default_val: Fallback numeric value if key is not present.
            :return: Resolved configuration float value.
        '''
        return self.read_settings().get(key, default_val)
