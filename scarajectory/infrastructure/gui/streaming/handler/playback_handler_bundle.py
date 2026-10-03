# -*- coding: UTF-8 -*-

'''
Module
    playback_handler_bundle.py
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
    Parameter bundle holding dependencies for StreamPlaybackActionHandler.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.connection.istream_connection import IStreamConnection
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.core.service.trajectory.plan.itrajectory_read_only import ITrajectoryReadOnly
from scarajectory.infrastructure.gui.connection.port_connection_panel import PortConnectionPanel
from scarajectory.infrastructure.gui.streaming.panel.stream_progress_adapter import StreamProgressAdapter

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class PlaybackHandlerBundle:
    '''
        Parameter bundle holding dependencies for StreamPlaybackActionHandler.

        It defines:

            :attributes:
                | plan - Active trajectory plan read-only abstraction.
                | validator - Kinematic reachability validator.
                | connection - Stream transport connection controller.
                | playback_controller - Motion trajectory playback controller.
                | progress_adapter - UI adapter synchronizing stream state.
                | port_panel - Serial port connection subpanel.
    '''

    plan: ITrajectoryReadOnly
    validator: ITrajectoryValidator
    connection: IStreamConnection
    playback_controller: IStreamPlaybackController
    progress_adapter: StreamProgressAdapter
    port_panel: PortConnectionPanel
