# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_streamer.py
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
    Defines interface ITrajectoryStreamer for robot communication and motion streaming.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable
from collections.abc import Sequence

from scarajectory.core.model.waypoint import Waypoint
from scarajectory.core.model.stream_config import StreamConfig
from scarajectory.core.service.istream_observer import IStreamObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryStreamer(Protocol):
    '''
        Contract for robot communication and flow-controlled trajectory streamers.

        It defines:

            :methods:
                | set_observer - Sets or updates the streaming progress observer.
                | is_connected - Checks if communication connection is open.
                | connect_with_config - Opens connection to robot with config DTO.
                | disconnect - Closes active connection.
                | start_streaming - Starts streaming sequence of waypoints to the robot.
                | pause_streaming - Pauses transmission.
                | resume_streaming - Resumes transmission.
                | stop_streaming - Aborts streaming and sends E-STOP.
                | send_raw_command - Sends single immediate command string.
    '''

    def set_observer(self, observer: IStreamObserver) -> None:
        '''
            Sets or updates the streaming progress observer.

            :param observer: IStreamObserver instance.
        '''

    def is_connected(self) -> bool:
        '''
            Checks if communication connection is open.

            :return: True if connected, False otherwise.
        '''

    def connect_with_config(self, config: StreamConfig) -> bool:
        '''
            Opens connection to robot with config DTO.

            :param config: StreamConfig parameters.
            :return: True if connected successfully.
        '''

    def disconnect(self) -> None:
        '''
            Closes active connection.
        '''

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
            Starts streaming sequence of waypoints to the robot.

            :param waypoints: Sequence of Waypoint instances.
            :return: True if streaming started.
        '''

    def pause_streaming(self) -> None:
        '''
            Pauses transmission.
        '''

    def resume_streaming(self) -> None:
        '''
            Resumes transmission.
        '''

    def stop_streaming(self) -> None:
        '''
            Aborts streaming and sends E-STOP.
        '''

    def send_raw_command(self, cmd: str) -> None:
        '''
            Sends single immediate command string.

            :param cmd: Raw command string.
        '''
