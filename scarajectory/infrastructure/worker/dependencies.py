# -*- coding: UTF-8 -*-

'''
Module
    dependencies.py
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
    Parameter bundle holding external dependencies for worker subsystem.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaracom.bridge.transceiver.ibyte_sender import IByteSender

from scarajectory.core.model.streaming.pacing_config import StreamPacingConfig
from scarajectory.core.service.streaming.observer.idispatcher import IStreamObserverDispatcher
from scarajectory.infrastructure.pacing.provides import PacingProvides
from scarajectory.infrastructure.packet.istrategy import IPacketStrategy
from scarajectory.infrastructure.state.imachine import IStreamStateMachine
from scarajectory.infrastructure.worker.parser.bundle import ParserBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class WorkerDependencies:
    '''
        Immutable parameter bundle holding external dependencies for worker subsystem.

        It defines:

            :attributes:
                | pacing_bundle - PacingProvides holding flow pacing and barrier collaborators.
                | packet_strategy - IPacketStrategy encoding waypoints to binary frames.
                | byte_sender - IByteSender transmitting raw byte stream to transport.
                | state_controller - IStreamStateMachine managing stream lifecycle state.
                | observer_dispatcher - IStreamObserverDispatcher publishing telemetry progress.
                | pacing_config - StreamPacingConfig containing loop delay intervals.
                | parser_bundle - ParserBundle holding binary parser and unpacker.
    '''

    pacing_bundle: PacingProvides
    packet_strategy: IPacketStrategy
    byte_sender: IByteSender
    state_controller: IStreamStateMachine
    observer_dispatcher: IStreamObserverDispatcher
    pacing_config: StreamPacingConfig
    parser_bundle: ParserBundle
