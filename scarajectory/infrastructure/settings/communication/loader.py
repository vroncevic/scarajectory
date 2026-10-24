# -*- coding: UTF-8 -*-

'''
Module
    loader.py
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
    Infrastructure adapter for loading communication and pacing settings.
'''

from __future__ import annotations

from collections.abc import Mapping
from os.path import abspath, dirname, exists, join
from typing import ClassVar, Final

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.config_factory import ConfigFactory
from scarajectory.core.service.streaming.pacing_config_factory import StreamPacingConfigFactory
from scarajectory.infrastructure.storage.config_io.loader.iloader import IConfigLoader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CommunicationSettingsLoader:
    '''
        Settings adapter loading and constructing communication and pacing models.

        It defines:

            :attributes:
                | DEFAULT_COMMUNICATION_CONFIG - Default absolute path to communication.json.
                | DEFAULT_SCHEME_CONFIG - Default absolute path to communication_scheme.json.
                | _config_path - Absolute path to communication configuration file.
                | _scheme_path - Absolute path to validation schema file.
                | _config_loader - Injected IConfigLoader protocol collaborator.
                | _cached_settings - Cached raw configuration dictionary.

            :methods:
                | __init__ - Initializes CommunicationSettingsLoader with file paths and loader.
                | read_settings - Loads and caches raw dictionary of settings.
                | load_stream_config - Constructs StreamConfig domain model from settings.
                | load_stream_config_with_options - Constructs StreamConfig with custom options.
                | load_pacing_config - Constructs StreamPacingConfig model from settings.
                | load_pacing_config_with_options - Constructs StreamPacingConfig with custom options.
    '''

    DEFAULT_COMMUNICATION_CONFIG: ClassVar[str] = join(
        dirname(dirname(dirname(abspath(__file__)))), 'config', 'communication.json'
    )
    DEFAULT_SCHEME_CONFIG: ClassVar[str] = join(
        dirname(dirname(dirname(abspath(__file__)))), 'config', 'communication_scheme.json'
    )

    _config_path: str
    _scheme_path: str
    _config_loader: IConfigLoader
    _cached_settings: dict[str, object]

    def __init__(
        self,
        *,
        config_path: str,
        scheme_path: str,
        config_loader: IConfigLoader,
    ) -> None:
        '''
            Initializes CommunicationSettingsLoader with file paths and loader.

            :param config_path: Absolute path to communication configuration file.
            :param scheme_path: Absolute path to validation schema file.
            :param config_loader: Injected IConfigLoader instance.
            :exceptions: None.
        '''
        self._config_path: Final[str] = config_path
        self._scheme_path: Final[str] = scheme_path
        self._config_loader: Final[IConfigLoader] = config_loader
        self._cached_settings = {}

    def read_settings(self) -> dict[str, object]:
        '''
            Reads and returns configuration parameters dictionary using configuration loader.

            :return: Dictionary containing configuration key-value mappings.
            :exceptions: None.
        '''
        if bool(self._cached_settings):
            return self._cached_settings

        if not exists(self._config_path):
            return {}

        data: object = self._config_loader.load_validated(
            filepath=self._config_path,
            scheme_path=self._scheme_path,
        )

        if isinstance(data, dict):
            self._cached_settings = dict(data)

        return self._cached_settings

    def load_stream_config(self) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration.

            :return: Configured StreamConfig domain model.
            :exceptions: None.
        '''
        return self.load_stream_config_with_options(options={})

    def load_stream_config_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance with custom options overriding configuration.

            :param options: Key-value options overriding base configuration.
            :return: Configured StreamConfig domain model.
            :exceptions: None.
        '''
        cfg: dict[str, object] = self.read_settings()
        merged: dict[str, object] = dict(cfg)
        merged.update(options)

        default_cfg: StreamConfig = ConfigFactory.create_default()
        resolved_port: str = (
            str(merged['port'])
            if 'port' in merged and isinstance(merged['port'], str)
            else default_cfg.port
        )
        resolved_baudrate: int = (
            int(merged['baudrate'])
            if 'baudrate' in merged and isinstance(merged['baudrate'], (int, float))
            else default_cfg.baudrate
        )
        resolved_timeout: float = (
            float(merged['timeout'])
            if 'timeout' in merged and isinstance(merged['timeout'], (int, float))
            else default_cfg.timeout
        )
        resolved_queue_capacity: int = (
            int(merged['queue_capacity'])
            if 'queue_capacity' in merged and isinstance(merged['queue_capacity'], (int, float))
            else default_cfg.queue_capacity
        )

        return StreamConfig(
            port=resolved_port,
            baudrate=resolved_baudrate,
            timeout=resolved_timeout,
            queue_capacity=resolved_queue_capacity,
        )

    def load_pacing_config(self) -> StreamPacingConfig:
        '''
            Constructs and returns StreamPacingConfig instance from configuration.

            :return: Configured StreamPacingConfig domain model.
            :exceptions: None.
        '''
        return self.load_pacing_config_with_options(options={})

    def load_pacing_config_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> StreamPacingConfig:
        '''
            Constructs and returns StreamPacingConfig instance with custom options overriding configuration.

            :param options: Key-value options overriding base configuration.
            :return: Configured StreamPacingConfig domain model.
            :exceptions: None.
        '''
        cfg: dict[str, object] = self.read_settings()
        merged: dict[str, object] = dict(cfg)
        merged.update(options)

        default_pacing: StreamPacingConfig = StreamPacingConfigFactory.create_binary()
        resolved_send_delay: float = (
            float(merged['send_delay'])
            if 'send_delay' in merged and isinstance(merged['send_delay'], (int, float))
            else default_pacing.send_delay
        )
        resolved_throttle_delay: float = (
            float(merged['throttle_delay'])
            if 'throttle_delay' in merged and isinstance(merged['throttle_delay'], (int, float))
            else default_pacing.throttle_delay
        )
        resolved_poll_delay: float = (
            float(merged['poll_delay'])
            if 'poll_delay' in merged and isinstance(merged['poll_delay'], (int, float))
            else default_pacing.poll_delay
        )

        return StreamPacingConfig(
            send_delay=resolved_send_delay,
            throttle_delay=resolved_throttle_delay,
            poll_delay=resolved_poll_delay,
        )
