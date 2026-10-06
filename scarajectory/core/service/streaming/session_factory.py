# -*- coding: UTF-8 -*-

'''
Module
    session_factory.py
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
    Factory service constructing StreamSession domain model instances.
'''

from __future__ import annotations

from collections.abc import Sequence

from scarajectory.core.model.state.stream_session import StreamSession
from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SessionFactory:
    '''
        Factory providing instantiation of StreamSession domain models.

        It defines:

            :methods:
                | create - Constructs StreamSession instance with explicit or default values.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        waypoints: Sequence[Waypoint] = (),
        sent_count: int = 0,
        done_count: int = 0,
        failed_count: int = 0,
        remote_queue_depth: int = 0,
        start_time: float = 0.0,
    ) -> StreamSession:
        '''
            Constructs StreamSession instance with provided parameters.

            :param waypoints: Initial sequence of waypoints.
            :param sent_count: Number of sent items.
            :param done_count: Number of completed items.
            :param failed_count: Number of failed items.
            :param remote_queue_depth: Microcontroller queue depth.
            :param start_time: Streaming start timestamp.
            :return: StreamSession instance.
            :exceptions: None.
        '''
        return StreamSession(
            waypoints=list(waypoints),
            sent_count=sent_count,
            done_count=done_count,
            failed_count=failed_count,
            remote_queue_depth=remote_queue_depth,
            start_time=start_time,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
