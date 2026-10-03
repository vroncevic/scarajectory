# -*- coding: UTF-8 -*-

'''
Module
    app_runtime_bundle.py
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
    Immutable value bundle holding runtime infrastructure subsystems.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.infrastructure.preferences.connection_repository import ConnectionRepository
from scarajectory.infrastructure.storage.plan_storage_service import PlanStorageService
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.infrastructure.transport.bundle import TransportBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class AppRuntimeBundle:
    '''
    Bundle containing assembled runtime infrastructure adapters.

    It defines:

        :attributes:
            | connection_repo - Preferences storage for connections.
            | transport - TransportBundle communication layer services.
            | streaming - StreamingBundle real-time dispatch services.
            | storage - PlanStorageService disk persistence interactor.
        :methods:
            | streamer - Returns playback controller for backward compatibility.
    '''

    connection_repo: ConnectionRepository
    transport: TransportBundle
    streaming: StreamingBundle
    storage: PlanStorageService

    @property
    def streamer(self) -> IStreamPlaybackController:
        '''
        Returns motion streaming playback controller.

        :return: IStreamPlaybackController instance.
        '''
        return self.streaming.playback_controller
