# -*- coding: UTF-8 -*-

'''
Module
    iconfig_factory.py
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
    Defines structural protocol IConfigFactory for creating StreamConfig models.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.communication.protocol.protocol_mode import ProtocolMode
from scarajectory.core.model.communication.stream.stream_config import StreamConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IConfigFactory(Protocol):
    '''
        Structural protocol defining factory interface for StreamConfig instances.

        It defines:

            :methods:
                | create - Builds StreamConfig model instance.
    '''

    def create(
        self,
        *,
        port: str,
        baudrate: int,
        timeout: float,
        queue_capacity: int,
        protocol_mode: ProtocolMode,
    ) -> StreamConfig:
        '''
            Builds StreamConfig model instance.

            :param port: Communication port.
            :param baudrate: Serial baudrate frequency.
            :param timeout: Communication timeout.
            :param queue_capacity: Microcontroller queue capacity.
            :param protocol_mode: Active protocol mode enum.
            :return: Configured StreamConfig model.
        '''
