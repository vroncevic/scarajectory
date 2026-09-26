# -*- coding: UTF-8 -*-

'''
Module
    imotion_streamer.py
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
    Defines structural protocol IMotionStreamer for trajectory and binary motion streaming.
'''

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from scaralang.core.model.dsl.binary.program import Program
from scarajectory.core.model.trajectory.waypoint import Waypoint

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IMotionStreamer(Protocol):
    '''
        Structural protocol defining motion trajectory and binary program streaming.

        It defines:

            :methods:
                | start_streaming - Starts streaming sequence of waypoints to the robot.
                | stream_binary_program - Streams pre-compiled Program directly to hardware.
                | pause_streaming - Pauses background streaming transmission.
                | resume_streaming - Resumes paused background streaming transmission.
                | stop_streaming - Aborts active streaming session and triggers E-STOP.
    '''

    def start_streaming(self, waypoints: Sequence[Waypoint]) -> bool:
        '''
            Starts streaming sequence of waypoints to the robot.

            :param waypoints: Sequence of Waypoint instances.
            :return: True if streaming started, False otherwise.
        '''

    def stream_binary_program(self, program: Program) -> bool:
        '''
            Streams pre-compiled Program directly to hardware.

            :param program: Program containing steps and raw frames.
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
