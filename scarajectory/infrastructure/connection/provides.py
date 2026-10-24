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
    Provides container exposing connection subsystem interfaces.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaracom.bridge.coordinator.icoordinator import IConnectionCoordinator
from scaracom.bridge.transceiver.ichannel import IRawChannel
from scaracom.flow.router.irouter import IFrameRouter

from scarajectory.infrastructure.connection.dispatcher.idispatcher import IChannelDispatcher
from scarajectory.infrastructure.connection.manager.imanager import IConnectionManager

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True, slots=True)
class ConnectionProvides:
    '''
        Immutable container providing connection subsystem interfaces.

        It defines:

            :attributes:
                | connection_manager - Injected IConnectionManager protocol instance.
                | raw_channel - Injected IRawChannel protocol instance.
                | channel_dispatcher - Injected IChannelDispatcher protocol instance.
                | frame_router - Injected IFrameRouter protocol instance.
                | connection_coordinator - Injected IConnectionCoordinator protocol instance.
    '''

    connection_manager: IConnectionManager
    raw_channel: IRawChannel
    channel_dispatcher: IChannelDispatcher
    frame_router: IFrameRouter
    connection_coordinator: IConnectionCoordinator
