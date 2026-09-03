# -*- coding: UTF-8 -*-

'''
Module
    istream_observer.py
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
    Defines IStreamObserver receiving real-time streaming progress updates.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.stream_progress import StreamProgress

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.2'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamObserver(Protocol):
    '''
        Observer receiving real-time streaming progress updates.

        It defines:

            :methods:
                | on_stream_progress - Called whenever a packet is sent, acked or completed.
                | on_serial_log - Called when a serial packet is transmitted or received.
    '''

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Called whenever a packet is sent, acked or completed.

            :param progress: StreamProgress metric container.
            :exceptions: None.
        '''

    def on_serial_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Called when a serial packet is transmitted or received.

            :param text: Message string content.
            :param is_outgoing: True if transmitted by host, False if received from robot.
            :exceptions: None.
        '''
