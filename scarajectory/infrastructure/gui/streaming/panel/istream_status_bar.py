# -*- coding: UTF-8 -*-

'''
Module
    istream_status_bar.py
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
    Defines structural protocol IStreamStatusBar for streamer status indicators.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.telemetry.stream_progress import StreamProgress

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IStreamStatusBar(Protocol):
    '''
        Structural protocol for streamer progress bar and status label widget.

        It defines:

            :methods:
                | set_status_text - Updates the informational status label text.
                | update_progress - Updates progress indicators from stream progress model.
    '''

    def set_status_text(self, text: str) -> None:
        '''
            Sets the status bar label text directly.

            :param text: Informational status text string.
            :exceptions: None.
        '''

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates progress bar and formatted metrics from progress model.

            :param progress: StreamProgress data model.
            :exceptions: None.
        '''
