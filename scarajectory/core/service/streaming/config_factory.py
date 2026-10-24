# -*- coding: UTF-8 -*-

'''
Module
    config_factory.py
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
    Factory service constructing StreamConfig domain models from settings or defaults.
'''

from __future__ import annotations

from typing import ClassVar

from scarajectory.core.model.streaming.config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ConfigFactory:
    '''
        Factory providing creation of StreamConfig parameter models.

        It defines:

            :constants:
                | DEFAULT_PORT - Default serial port device path.
                | DEFAULT_BAUDRATE - Default baudrate frequency.
                | DEFAULT_TIMEOUT - Default communication timeout in seconds.
                | DEFAULT_QUEUE_CAPACITY - Default remote ring buffer queue capacity.
            :methods:
                | create_default - Constructs StreamConfig with standard default parameters.
                | create - Constructs StreamConfig using explicit configuration parameters.
                | get_version - Returns factory version string.
    '''

    DEFAULT_PORT: ClassVar[str] = '/dev/ttyUSB0'
    DEFAULT_BAUDRATE: ClassVar[int] = 115200
    DEFAULT_TIMEOUT: ClassVar[float] = 0.1
    DEFAULT_QUEUE_CAPACITY: ClassVar[int] = 16

    @classmethod
    def create_default(cls) -> StreamConfig:
        '''
            Constructs and returns a StreamConfig instance with standard default parameters.

            :return: Default StreamConfig model instance.
            :exceptions: None.
        '''
        return StreamConfig(
            port=cls.DEFAULT_PORT,
            baudrate=cls.DEFAULT_BAUDRATE,
            timeout=cls.DEFAULT_TIMEOUT,
            queue_capacity=cls.DEFAULT_QUEUE_CAPACITY,
        )

    @classmethod
    def create(
        cls,
        *,
        port: str,
        baudrate: int,
    ) -> StreamConfig:
        '''
            Constructs and returns a StreamConfig instance with explicit parameters.

            :param port: Communication port path or IP:port address.
            :param baudrate: Baudrate frequency integer.
            :return: Configured StreamConfig model instance.
            :exceptions: None.
        '''
        return StreamConfig(
            port=port,
            baudrate=baudrate,
            timeout=cls.DEFAULT_TIMEOUT,
            queue_capacity=cls.DEFAULT_QUEUE_CAPACITY,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
