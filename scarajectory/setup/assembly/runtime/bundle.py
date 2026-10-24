# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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

from scaracom.transport.preference.irepository import ISerialPreferenceRepository
from scaracom.transport.itransport import ITransport

from scarajectory.core.service.storage.iloader import IPlanLoader
from scarajectory.core.service.storage.istorer import IPlanStorer
from scarajectory.core.service.streaming.playback.icontroller import IPlaybackController
from scarajectory.infrastructure.storage.workspace.imanager import IWorkspaceManager
from scarajectory.infrastructure.streaming.provides import StreamingProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
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
            | transport - ITransport communication layer instance.
            | streaming - StreamingProvides real-time dispatch services.
            | loader - IPlanLoader plan and file reader port.
            | storer - IPlanStorer plan and file writer port.
            | workspace - User workspace manager for script examples.
        :methods:
            | streamer - Returns playback controller for backward compatibility.
    '''

    connection_repo: ISerialPreferenceRepository
    transport: ITransport
    streaming: StreamingProvides
    loader: IPlanLoader
    storer: IPlanStorer
    workspace: IWorkspaceManager

    @property
    def streamer(self) -> IPlaybackController:
        '''
        Returns motion streaming playback controller.

        :return: IPlaybackController instance.
        '''
        return self.streaming.playback_controller
