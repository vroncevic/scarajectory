# -*- coding: UTF-8 -*-

'''
Module
    stream_control_panel.py
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
    Trajectory streaming execution and emergency stop control panel component.
'''

from __future__ import annotations

from collections.abc import Callable
from tkinter import LEFT, Widget
from tkinter.ttk import Button, Frame

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlPanel(Frame):
    '''
        Stream execution buttons panel providing Start, Pause/Resume, and E-STOP triggers.

        It defines:

            :methods:
                | __init__ - Initializes streaming control buttons layout.
    '''

    def __init__(
        self,
        parent: Widget,
        *,
        on_start_stream: Callable[[], None],
        on_pause_resume: Callable[[], None],
        on_stop: Callable[[], None],
        **kwargs: object,
    ) -> None:
        '''
            Initializes streaming control buttons layout.

            :param parent: Parent container widget.
            :param on_start_stream: Callback for initiating trajectory streaming.
            :param on_pause_resume: Callback for toggling pause and resume state.
            :param on_stop: Callback for emergency stopping transmission.
            :exceptions: None.
        '''
        super().__init__(parent, **kwargs)

        Button(
            self,
            text='Stream to Robot',
            style='Success.TButton',
            command=on_start_stream,
        ).pack(side=LEFT, padx=3)

        Button(
            self,
            text='Pause / Resume',
            command=on_pause_resume,
        ).pack(side=LEFT, padx=3)

        Button(
            self,
            text='Stop / E-STOP',
            style='Danger.TButton',
            command=on_stop,
        ).pack(side=LEFT, padx=3)
