# -*- coding: UTF-8 -*-

'''
Module
    iserial_streamer.py
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
    Defines abstract interface ISerialStreamer for motion execution.
'''

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence

from scarajectory.core.model.studio_waypoint import StudioWaypoint
from scarajectory.core.model.stream_config_dto import StreamConfigDTO

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ISerialStreamer(ABC):
    '''
        Contract for serial communication and flow-controlled packet streamers.

        It defines:

            :methods:
                | is_connected - Checks if serial connection is open.
                | connect_with_config - Opens connection to serial port with config DTO.
                | disconnect - Closes active serial connection.
                | start_streaming - Starts streaming sequence of waypoints to the robot.
                | pause_streaming - Pauses transmission.
                | resume_streaming - Resumes transmission.
                | stop_streaming - Aborts streaming and sends E-STOP.
                | send_raw_command - Sends single immediate command string.
    '''

    @abstractmethod
    def is_connected(self) -> bool:
        '''
            Checks if serial connection is open.

            :return: True if connected, False otherwise.
            :exceptions: None.
        '''

    @abstractmethod
    def connect_with_config(self, config: StreamConfigDTO) -> bool:
        '''
            Opens connection to serial port with config DTO.

            :param config: StreamConfigDTO parameters.
            :return: True if connected successfully.
            :exceptions: None.
        '''

    @abstractmethod
    def disconnect(self) -> None:
        '''
            Closes active serial connection.

            :exceptions: None.
        '''

    @abstractmethod
    def start_streaming(self, waypoints: Sequence[StudioWaypoint]) -> bool:
        '''
            Starts streaming sequence of waypoints to the robot.

            :param waypoints: Sequence of StudioWaypoint instances.
            :return: True if streaming started.
            :exceptions: None.
        '''

    @abstractmethod
    def pause_streaming(self) -> None:
        '''
            Pauses transmission.

            :exceptions: None.
        '''

    @abstractmethod
    def resume_streaming(self) -> None:
        '''
            Resumes transmission.

            :exceptions: None.
        '''

    @abstractmethod
    def stop_streaming(self) -> None:
        '''
            Aborts streaming and sends E-STOP.

            :exceptions: None.
        '''

    @abstractmethod
    def send_raw_command(self, cmd: str) -> None:
        '''
            Sends single immediate command string.

            :param cmd: Raw command string.
            :exceptions: None.
        '''
