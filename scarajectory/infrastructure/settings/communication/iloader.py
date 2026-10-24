# -*- coding: UTF-8 -*-

'''
Module
    iloader.py
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
    Interface protocol defining operations for loading communication settings.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from scarajectory.core.model.streaming.config import StreamConfig
from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICommunicationSettingsLoader(Protocol):
    '''
        Protocol defining communication settings loading operations.

        It defines:

            :methods:
                | read_settings - Reads raw settings dictionary from configuration file.
                | load_stream_config - Constructs StreamConfig domain model from settings.
                | load_stream_config_with_options - Constructs StreamConfig with custom options.
                | load_pacing_config - Constructs StreamPacingConfig model from settings.
                | load_pacing_config_with_options - Constructs StreamPacingConfig with custom options.
    '''

    def read_settings(self) -> dict[str, object]:
        '''
            Reads and returns configuration parameters dictionary using configuration loader.

            :return: Dictionary containing configuration key-value mappings.
        '''

    def load_stream_config(self) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration.

            :return: Configured StreamConfig domain model.
        '''

    def load_stream_config_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance with custom options overriding configuration.

            :param options: Key-value options overriding base configuration.
            :return: Configured StreamConfig domain model.
        '''

    def load_pacing_config(self) -> StreamPacingConfig:
        '''
            Constructs and returns StreamPacingConfig instance from configuration.

            :return: Configured StreamPacingConfig domain model.
        '''

    def load_pacing_config_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> StreamPacingConfig:
        '''
            Constructs and returns StreamPacingConfig instance with custom options overriding configuration.

            :param options: Key-value options overriding base configuration.
            :return: Configured StreamPacingConfig domain model.
        '''
