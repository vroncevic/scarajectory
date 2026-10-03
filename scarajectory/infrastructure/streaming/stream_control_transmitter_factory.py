# -*- coding: UTF-8 -*-

'''
Module
    stream_control_transmitter_factory.py
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
    Factory for creating StreamControlTransmitter instances.
'''

from __future__ import annotations

from scaralang.core.service.protocol.ibinary_frame_builder import IBinaryFrameBuilder
from scarajectory.infrastructure.connection.istream_raw_transceiver import IStreamRawTransceiver
from scarajectory.infrastructure.streaming.stream_control_transmitter import StreamControlTransmitter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlTransmitterFactory:
    '''
    Factory for creating StreamControlTransmitter instances.

    It defines:

        :methods:
            | create - Constructs StreamControlTransmitter instance.
            | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        raw_transceiver: IStreamRawTransceiver,
        frame_builder: IBinaryFrameBuilder,
    ) -> StreamControlTransmitter:
        '''
        Constructs StreamControlTransmitter instance with injected dependencies.

        :param raw_transceiver: Injected IStreamRawTransceiver instance.
        :param frame_builder: Injected IBinaryFrameBuilder instance.
        :return: Fresh StreamControlTransmitter instance.
        '''
        return StreamControlTransmitter(
            raw_transceiver=raw_transceiver,
            frame_builder=frame_builder,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
        Returns factory version string.

        :return: Factory version string.
        '''
        return __version__
