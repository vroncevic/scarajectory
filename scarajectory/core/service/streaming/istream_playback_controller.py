# -*- coding: UTF-8 -*-

'''
Module
    istream_playback_controller.py
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
    Defines structural protocol IStreamPlaybackController for streaming playback lifecycle.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamPlaybackController(Protocol):
    '''
        Structural protocol defining streaming playback lifecycle control.

        It defines:

            :methods:
                | start_streaming - Starts background streaming worker with sequence of waypoints.
                | pause_streaming - Pauses background streaming transmission.
                | resume_streaming - Resumes paused background streaming transmission.
                | stop_streaming - Aborts active streaming session and triggers E-STOP.
    '''

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
            Starts background streaming worker with sequence of waypoints.

            :param waypoints: Sequence of Waypoint instances.
            :return: True if streaming started, False otherwise.
        '''

    def pause_streaming(self) -> None:
        '''
            Pauses background streaming transmission.
        '''

    def resume_streaming(self) -> None:
        '''
            Resumes paused background streaming transmission.
        '''

    def stop_streaming(self) -> None:
        '''
            Aborts active streaming session and triggers E-STOP.
        '''
