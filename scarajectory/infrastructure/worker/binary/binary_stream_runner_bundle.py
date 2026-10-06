# -*- coding: UTF-8 -*-

'''
Module
    binary_stream_runner_bundle.py
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
    Parameter bundle holding collaborators for binary streaming workers and loop runners.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.model.streaming.stream_pacing_config import StreamPacingConfig
from scarajectory.infrastructure.packet.ipacket_strategy import IPacketStrategy
from scarajectory.infrastructure.state.istream_state_controller import IStreamStateController
from scarajectory.core.service.streaming.observer.istream_observer_dispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.connection.ibyte_sender import IByteSender
from scarajectory.infrastructure.pacing.bundle import FlowPacingBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class BinaryStreamRunnerBundle:
    '''
        Immutable parameter bundle holding collaborators for binary stream worker and loop runner.

        It defines:

            :attributes:
                | pacing_bundle - FlowPacingBundle managing flow pacing and barrier coordination.
                | packet_strategy - IPacketStrategy encoding waypoints to binary frames.
                | byte_sender - IByteSender transmitting raw byte stream to transport.
                | state_controller - IStreamStateController managing stream lifecycle state.
                | observer_dispatcher - IStreamObserverDispatcher publishing telemetry progress.
                | pacing_config - StreamPacingConfig containing loop delay intervals.
    '''

    pacing_bundle: FlowPacingBundle
    packet_strategy: IPacketStrategy
    byte_sender: IByteSender
    state_controller: IStreamStateController
    observer_dispatcher: IStreamObserverDispatcher
    pacing_config: StreamPacingConfig
