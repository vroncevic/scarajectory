# -*- coding: UTF-8 -*-

'''
Module
    istream_execution_service.py
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
    Defines interface IStreamExecutionService for trajectory hardware streaming execution.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamExecutionService(Protocol):
    '''
        Interface for controlling hardware streaming execution lifecycle.

        It defines:

            :methods:
                | start_streaming - Initiates streaming of current plan.
                | stop_streaming - Aborts active streaming.
                | pause_streaming - Pauses active trajectory streaming.
                | resume_streaming - Resumes paused trajectory streaming.
    '''

    def start_streaming(self) -> bool:
        '''
            Initiates streaming of current plan.

            :return: True if stream started, False otherwise.
        '''

    def stop_streaming(self) -> None:
        '''
            Aborts active streaming.
        '''

    def pause_streaming(self) -> None:
        '''
            Pauses active trajectory streaming.
        '''

    def resume_streaming(self) -> None:
        '''
            Resumes paused trajectory streaming.
        '''
