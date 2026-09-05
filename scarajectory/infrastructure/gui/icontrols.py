# -*- coding: UTF-8 -*-

'''
Module
    icontrols.py
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
    Defines interface IControls for multi-tab control panels.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.stream_progress import StreamProgress

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IControls(Protocol):
    '''
        Interface for robot streamer, validation, and jog control panels.

        It defines:

            :methods:
                | refresh_ports - Updates available serial ports list.
                | append_log - Appends message to terminal log console.
                | update_progress - Updates streamer progress bar and metrics.
    '''

    def refresh_ports(self) -> None:
        '''
            Updates available serial ports list.
        '''

    def append_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Appends message to terminal log console.

            :param text: Message string.
            :param is_outgoing: Flag indicating outgoing transmission.
        '''

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates streamer progress bar and metrics.

            :param progress: StreamProgress metric container.
        '''
