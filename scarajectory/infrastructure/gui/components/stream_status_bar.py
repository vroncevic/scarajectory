# -*- coding: UTF-8 -*-

'''
Module
    stream_status_bar.py
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
    Status indicator bar rendering streamer progress bar and text summary.
'''

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from scarajectory.core.model.stream_progress import StreamProgress

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.1'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamStatusBar(ttk.Frame):
    '''
        Streamer progress bar and summary label widget.

        It defines:

            :attributes:
                | _progress_bar - Tkinter progress bar widget.
                | _lbl_status - Summary status text label.
            :methods:
                | __init__ - Initializes status bar layout.
                | set_status_text - Sets label text directly.
                | update_progress - Updates progress bar and formatted status text.
    '''

    _progress_bar: ttk.Progressbar
    _lbl_status: ttk.Label

    def __init__(self, parent: tk.Widget, **kwargs: object) -> None:
        '''
            Initializes status bar layout.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)
        self._create_widgets()

    def _create_widgets(self) -> None:
        '''
            Builds progress bar and summary label.

            :exceptions: None.
        '''
        self._progress_bar = ttk.Progressbar(self, maximum=100.0)
        self._progress_bar.pack(fill=tk.X, pady=3)

        self._lbl_status = ttk.Label(self, text='Streamer: Disconnected', font=('DejaVu Sans', 9, 'bold'))
        self._lbl_status.pack(anchor='w')

    def set_status_text(self, text: str) -> None:
        '''
            Sets label text directly.

            :param text: Text string to display.
            :exceptions: None.
        '''
        self._lbl_status.configure(text=text)

    def update_progress(self, progress: StreamProgress) -> None:
        '''
            Updates progress bar and formatted status text.

            :param progress: StreamProgress data model.
            :exceptions: None.
        '''
        pct: float = (progress.completed_waypoints / progress.total_waypoints * 100.0) if progress.total_waypoints > 0 else 0.0
        self._progress_bar['value'] = pct
        self._lbl_status.configure(
            text=(
                f'Status: {progress.state.value} | Pts: {progress.completed_waypoints}/{progress.total_waypoints} '
                f'({pct:.0f}%) | Time: {progress.elapsed_seconds:.1f}s'
            )
        )
