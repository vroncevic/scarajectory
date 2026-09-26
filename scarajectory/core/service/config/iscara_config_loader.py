# -*- coding: UTF-8 -*-

'''
Module
    iscara_config_loader.py
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
    Defines abstract interface for loading robot geometry and transmission configurations.
'''

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.stream.stream_config import StreamConfig
from scarajectory.core.model.kinematics.scara_bounds import ScaraBounds
from scarajectory.core.model.kinematics.transmission_parameters import TransmissionParameters

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IScaraConfigLoader(Protocol):
    '''
        Protocol defining contract for reading SCARA geometry and transmission settings.

        It defines:

            :methods:
                | load_raw_config - Returns dictionary of raw loaded configuration keys.
                | load_bounds - Constructs ScaraBounds domain model from configuration.
                | load_bounds_with_options - Constructs ScaraBounds with override options.
                | load_transmission - Constructs TransmissionParameters from configuration.
                | load_transmission_with_options - Constructs TransmissionParameters with options.
                | load_stream_config - Constructs StreamConfig domain model from configuration.
                | load_stream_config_with_options - Constructs StreamConfig with override options.
    '''

    def load_raw_config(self) -> dict[str, float]:
        '''
            Reads and returns raw configuration key-value mappings.

            :return: Dictionary containing configuration floats.
        '''

    def load_bounds(self) -> ScaraBounds:
        '''
            Constructs and returns ScaraBounds domain model from configuration.

            :return: Configured ScaraBounds domain model.
        '''

    def load_bounds_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> ScaraBounds:
        '''
            Constructs and returns ScaraBounds instance with custom override options.

            :param options: Key-value options overriding base configuration.
            :return: Configured ScaraBounds domain model.
        '''

    def load_transmission(self) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters domain model from configuration.

            :return: Configured TransmissionParameters domain model.
        '''

    def load_transmission_with_options(
        self,
        *,
        options: Mapping[str, object],
    ) -> TransmissionParameters:
        '''
            Constructs and returns TransmissionParameters instance with custom override options.

            :param options: Key-value options overriding base configuration.
            :return: Configured TransmissionParameters domain model.
        '''

    def load_stream_config(self, *, port: str) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance from configuration for target port.

            :param port: Target port identifier.
            :return: Configured StreamConfig domain model.
        '''

    def load_stream_config_with_options(
        self,
        *,
        port: str,
        options: Mapping[str, object],
    ) -> StreamConfig:
        '''
            Constructs and returns StreamConfig instance with custom override options.

            :param port: Target port identifier.
            :param options: Key-value options overriding base configuration.
            :return: Configured StreamConfig domain model.
        '''
