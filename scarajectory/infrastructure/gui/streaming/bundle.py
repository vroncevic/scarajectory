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
    Parameter bundle holding dependencies for StreamerTab construction.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.connection.istream_connection import IStreamConnection
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.infrastructure.gui.streaming.streamer_controllers_bundle import StreamerControllersBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class StreamerBundle:
    '''
        Immutable container holding dependencies for StreamerTab assembly.

        It defines:

            :attributes:
                | plan - Active trajectory plan read-only abstraction.
                | validator - Kinematic reachability validator port.
                | connection - Stream transport connection controller.
                | playback_controller - Motion trajectory playback controller.
                | connection_repository - Connection preferences repository.
                | controllers - Injected manipulator sub-controllers bundle.
    '''

    plan: ITrajectoryReadOnly
    validator: ITrajectoryValidator
    connection: IStreamConnection
    playback_controller: IStreamPlaybackController
    connection_repository: IConnectionRepository
    controllers: StreamerControllersBundle
