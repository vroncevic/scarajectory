# -*- coding: UTF-8 -*-

'''
Module
    provides.py
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
    Outbound provides container exposing streaming subsystem services.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.core.service.streaming.observer.iregistry import IStreamObserverRegistry
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager
from scarajectory.infrastructure.streaming.binary.istreamer import IBinaryStreamer

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class StreamingProvides:
    '''
    Immutable container exposing public artifacts provided by streaming subsystem.

    It defines:

        :attributes:
            | connection_manager - IConnectionManager transport connection controller.
            | raw_channel - IRawChannel immediate command and byte transmitter.
            | playback_controller - IPlaybackController motion playback.
            | registry - IStreamObserverRegistry observer subscription port.
            | dispatcher - IStreamObserverDispatcher telemetry notification port.
            | binary_streamer - IBinaryStreamer compiled bytecode streamer.
    '''

    connection_manager: IConnectionManager
    raw_channel: IRawChannel
    playback_controller: IPlaybackController
    registry: IStreamObserverRegistry
    dispatcher: IStreamObserverDispatcher
    binary_streamer: IBinaryStreamer
