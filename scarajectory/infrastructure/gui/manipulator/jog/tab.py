# -*- coding: UTF-8 -*-

'''
Module
    tab.py
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
    Manual Jog control tab container for direct Cartesian and joint manipulation.
'''

from __future__ import annotations

from tkinter import Widget, X
from tkinter.ttk import Frame

from scarajectory.core.model.jog.axis import JogAxis
from scarajectory.infrastructure.gui.manipulator.jog.panel.bundle import JogPanelBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogTab(Frame):
    '''
        Manual jog tab orchestrating power, directional step grid, tooling, and raw command panels.

        It defines:

            :attributes:
                | _panels - Mounted sub-panel bundle.
            :methods:
                | __init__ - Initializes manual jog tab frame.
                | mount_panels - Mounts and packs power, jog grid, auxiliary toggles and raw panels.
                | panels - Returns mounted JogPanelBundle instance.
                | jog_step - Sends relative jog step along specified axis.
                | send_raw - Transmits text command from entry field over raw channel.
    '''

    _panels: JogPanelBundle

    def __init__(
        self,
        parent: Widget,
    ) -> None:
        '''
            Initializes manual jog controls container.

            :param parent: Parent container widget.
            :exceptions: None.
        '''
        super().__init__(parent, padding=6)

    def mount_panels(self, panels: JogPanelBundle) -> None:
        '''
            Mounts and packs power, jog grid, auxiliary toggles and raw panels.

            :param panels: Assembled JogPanelBundle instance.
            :exceptions: None.
        '''
        self._panels = panels

        panels.power_panel.pack(fill=X, pady=2)
        panels.axis_grid_panel.pack(fill=X, pady=2)
        panels.tool_panel.pack(fill=X, pady=4)
        panels.raw_panel.pack(fill=X, pady=2)

    @property
    def panels(self) -> JogPanelBundle:
        '''
            Returns mounted JogPanelBundle instance.

            :return: JogPanelBundle instance.
            :exceptions: None.
        '''
        return self._panels

    def jog_step(self, axis: JogAxis | str, sign: float = 1.0) -> None:
        '''
            Sends relative jog command based on selected step size.

            :param axis: Axis identifier (JogAxis enum or str).
            :param sign: Direction multiplier (+1.0 or -1.0).
            :exceptions: None.
        '''
        self._panels.axis_grid_panel.jog_step(axis, sign)

    def send_raw(self) -> None:
        '''
            Transmits raw command from text input to microcontroller.

            :exceptions: None.
        '''
        self._panels.raw_panel.send_raw()
