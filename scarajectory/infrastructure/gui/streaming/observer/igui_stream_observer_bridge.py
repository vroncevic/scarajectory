# -*- coding: UTF-8 -*-

'''
Module
    igui_stream_observer_bridge.py
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
    Defines structural protocol IGuiStreamObserverBridge for GUI streaming telemetry bridge.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.telemetry.stream_progress import StreamProgress

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IGuiStreamObserverBridge(Protocol):
    '''
        Structural protocol defining GUI thread bridge for streaming progress and logs.

        It defines:

            :methods:
                | on_stream_progress - Marshals streamer progress metrics to GUI thread.
                | on_serial_log - Marshals serial communication log messages to GUI thread.
    '''

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Marshals streamer progress metrics to GUI thread.

            :param progress: StreamProgress metric container.
            :exceptions: None.
        '''

    def on_serial_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Marshals serial communication log messages to GUI thread.

            :param text: Message string content.
            :param is_outgoing: True if transmitted by host, False if received from robot.
            :exceptions: None.
        '''
