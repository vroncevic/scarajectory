# -*- coding: UTF-8 -*-

'''
Module
    stream_config_loader.py
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
    Infrastructure adapter for loading StreamConfig communication settings.
'''

from __future__ import annotations

from collections.abc import Mapping

from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.streaming.stream_config import StreamConfig
from scarajectory.infrastructure.settings.isettings_reader import ISettingsReader

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamConfigLoader:
    '''
        Settings adapter loading and constructing StreamConfig domain models.

        It defines:

            :attributes:
                | _reader - Injected ISettingsReader providing configuration key-values.

            :methods:
                | __init__ - Initializes StreamConfigLoader with injected ISettingsReader.
                | load_stream_config - Constructs StreamConfig with default configuration for port.
                | load_stream_config_with_options - Constructs StreamConfig with custom override options.
    '''

    _reader: ISettingsReader

    def __init__(self, *, reader: ISettingsReader) -> None:
        '''
            Initializes StreamConfigLoader with injected ISettingsReader.

            :param reader: ISettingsReader instance.
        '''
        self._reader = reader

    def load_stream_config(self, *, port: str) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration for target port.

            :param port: Target serial device port or host string.
            :return: Configured StreamConfig domain model.
        '''
        return self.load_stream_config_with_options(port=port, options={})

    def load_stream_config_with_options(
        self,
        *,
        port: str,
        options: Mapping[str, object],
    ) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration and options.

            :param port: Target serial device port or host string.
            :param options: Key-value options overriding base configuration.
            :return: Configured StreamConfig domain model.
        '''
        cfg: dict[str, float] = self._reader.read_settings()

        baudrate: int = int(options.get('baudrate', cfg.get('baudrate', 115200.0)))
        timeout: float = float(options.get('timeout', cfg.get('timeout', 0.1)))
        queue_capacity: int = int(options.get('queue_capacity', cfg.get('queue_capacity', 16.0)))

        mode_val = options.get('protocol_mode', 'binary')
        mode: ProtocolMode = (
            mode_val
            if isinstance(mode_val, ProtocolMode)
            else ProtocolMode(str(mode_val))
        )

        return StreamConfig(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
            queue_capacity=queue_capacity,
            protocol_mode=mode,
        )
