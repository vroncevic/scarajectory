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

from tkinter import LEFT, Widget
from tkinter.ttk import Button, Frame
from typing import Final

from scarajectory.infrastructure.gui.streaming.panel.istream_control_delegate import IStreamControlDelegate

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StreamControlPanel(Frame):
    '''
        Stream execution buttons panel providing Start, Pause/Resume, and E-STOP triggers.

        It defines:

            :attributes:
                | _control_delegate - Injected action delegate handling stream execution commands.
            :methods:
                | __init__ - Initializes streaming control buttons layout.
    '''

    _control_delegate: IStreamControlDelegate

    def __init__(
        self,
        parent: Widget,
        *,
        control_delegate: IStreamControlDelegate,
    ) -> None:
        '''
            Initializes streaming control buttons layout.

            :param parent: Parent container widget.
            :param control_delegate: Injected IStreamControlDelegate action delegate.
            :exceptions: None.
        '''
        super().__init__(parent)
        self._control_delegate: Final[IStreamControlDelegate] = control_delegate

        Button(
            self,
            text='Stream to Robot',
            style='Success.TButton',
            command=self._control_delegate.on_start_stream,
        ).pack(side=LEFT, padx=3)

        Button(
            self,
            text='Pause / Resume',
            command=self._control_delegate.on_pause_resume_stream,
        ).pack(side=LEFT, padx=3)

        Button(
            self,
            text='Stop / E-STOP',
            style='Danger.TButton',
            command=self._control_delegate.on_stop_stream,
        ).pack(side=LEFT, padx=3)
