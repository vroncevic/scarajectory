# -*- coding: UTF-8 -*-

'''
Module
    stream_pacing_config_factory.py
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
    Factory service constructing StreamPacingConfig models for ASCII and Binary stream execution.
'''

from __future__ import annotations

from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamPacingConfigFactory:
    '''
        Factory providing construction of StreamPacingConfig parameter models.

        It defines:

            :methods:
                | create_ascii - Constructs StreamPacingConfig with ASCII protocol pacing delays.
                | create_binary - Constructs StreamPacingConfig with Binary protocol pacing delays.
                | create - Constructs StreamPacingConfig with explicit delay parameters.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create_ascii(cls) -> StreamPacingConfig:
        '''
            Constructs StreamPacingConfig with standard ASCII protocol pacing parameters.

            :return: StreamPacingConfig instance configured for ASCII streaming.
            :exceptions: None.
        '''
        return StreamPacingConfig(
            send_delay=0.01,
            throttle_delay=0.02,
            poll_delay=0.05,
        )

    @classmethod
    def create_binary(cls) -> StreamPacingConfig:
        '''
            Constructs StreamPacingConfig with standard Binary protocol pacing parameters.

            :return: StreamPacingConfig instance configured for Binary streaming.
            :exceptions: None.
        '''
        return StreamPacingConfig(
            send_delay=0.005,
            throttle_delay=0.01,
            poll_delay=0.02,
        )

    @classmethod
    def create(
        cls,
        *,
        send_delay: float,
        throttle_delay: float,
        poll_delay: float,
    ) -> StreamPacingConfig:
        '''
            Constructs StreamPacingConfig with explicit delay parameters.

            :param send_delay: Loop pacing delay after transmitting packet in seconds.
            :param throttle_delay: Delay when buffer queue is full in seconds.
            :param poll_delay: Polling interval during pause or completion wait in seconds.
            :return: Configured StreamPacingConfig model instance.
            :exceptions: None.
        '''
        return StreamPacingConfig(
            send_delay=send_delay,
            throttle_delay=throttle_delay,
            poll_delay=poll_delay,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
        '''
        return __version__
