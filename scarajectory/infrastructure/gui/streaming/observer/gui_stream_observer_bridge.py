# -*- coding: UTF-8 -*-

'''
Module
    gui_stream_observer_bridge.py
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
    Thread-safe observer bridge marshaling streamer events to Tkinter main loop.
'''

from __future__ import annotations

from tkinter import Tk
from typing import Final

from scarajectory.core.model.telemetry.stream_progress import StreamProgress
from scarajectory.infrastructure.gui.controls.icontrols_panel import IControlsPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class GuiStreamObserverBridge:
    '''
        Thread-safe observer bridge marshaling streamer events to Tkinter main loop.

        It defines:

            :attributes:
                | _root - Root Tkinter application window for thread dispatching.
                | _controls - Tabbed control panels component receiving UI updates.
            :methods:
                | __init__ - Initializes bridge with root window and controls component.
                | on_stream_progress - Marshals streamer progress metrics to GUI thread.
                | on_serial_log - Marshals serial communication log messages to GUI thread.
    '''

    _root: Tk
    _controls: IControlsPanel

    def __init__(self, root: Tk, controls: IControlsPanel) -> None:
        '''
            Initializes bridge with root window and controls component.

            :param root: Root Tk window for thread dispatching.
            :param controls: Injected IControlsPanel component.
            :exceptions: None.
        '''
        self._root: Final[Tk] = root
        self._controls: Final[IControlsPanel] = controls

    def on_stream_progress(self, progress: StreamProgress) -> None:
        '''
            Marshals streamer progress metrics to GUI thread via root.after.

            :param progress: StreamProgress metric container.
            :exceptions: None.
        '''
        self._root.after(0, self._controls.update_progress, progress)

    def on_serial_log(self, text: str, is_outgoing: bool = False) -> None:
        '''
            Marshals serial communication log messages to GUI thread via root.after.

            :param text: Message string content.
            :param is_outgoing: True if transmitted by host, False if received from robot.
            :exceptions: None.
        '''
        self._root.after(0, self._controls.append_log, text, is_outgoing)
