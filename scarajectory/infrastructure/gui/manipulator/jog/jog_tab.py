# -*- coding: UTF-8 -*-

'''
Module
    jog_tab.py
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

from scarajectory.core.model.jog.jog_axis import JogAxis
from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel import JogAxisGridPanel
from scarajectory.infrastructure.gui.manipulator.jog.panel_bundle import JogPanelBundle
from scarajectory.infrastructure.gui.manipulator.jog.power_panel import JogPowerPanel
from scarajectory.infrastructure.gui.manipulator.jog.raw_command_panel import JogRawCommandPanel
from scarajectory.infrastructure.gui.manipulator.jog.tool_panel import JogToolPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogTab(Frame):
    '''
        Manual jog tab orchestrating power, directional step grid, tooling, and raw command panels.

        It defines:

            :attributes:
                | _panels - Mounted sub-panel bundle.
                | _power_panel - Sub-panel for power and homing commands.
                | _axis_grid_panel - Sub-panel for directional jog steps and step size.
                | _tool_panel - Sub-panel for pneumatic pump and purge valve toggles.
                | _raw_panel - Sub-panel for raw ASCII micro-command transmission.
            :methods:
                | __init__ - Initializes manual jog tab frame.
                | mount_panels - Mounts and packs power, jog grid, auxiliary toggles and raw panels.
                | jog_step - Sends relative jog step along specified axis.
                | send_raw - Transmits text command from entry field over raw channel.
    '''

    _panels: JogPanelBundle
    _power_panel: JogPowerPanel
    _axis_grid_panel: JogAxisGridPanel
    _tool_panel: JogToolPanel
    _raw_panel: JogRawCommandPanel

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
        self._power_panel = panels.power_panel
        self._axis_grid_panel = panels.axis_grid_panel
        self._tool_panel = panels.tool_panel
        self._raw_panel = panels.raw_panel

        self._power_panel.pack(fill=X, pady=2)
        self._axis_grid_panel.pack(fill=X, pady=2)
        self._tool_panel.pack(fill=X, pady=4)
        self._raw_panel.pack(fill=X, pady=2)

    @property
    def power_panel(self) -> JogPowerPanel:
        '''
            Returns mounted JogPowerPanel instance.

            :return: JogPowerPanel instance.
            :exceptions: None.
        '''
        return self._power_panel

    @property
    def axis_grid_panel(self) -> JogAxisGridPanel:
        '''
            Returns mounted JogAxisGridPanel instance.

            :return: JogAxisGridPanel instance.
            :exceptions: None.
        '''
        return self._axis_grid_panel

    @property
    def tool_panel(self) -> JogToolPanel:
        '''
            Returns mounted JogToolPanel instance.

            :return: JogToolPanel instance.
            :exceptions: None.
        '''
        return self._tool_panel

    @property
    def raw_panel(self) -> JogRawCommandPanel:
        '''
            Returns mounted JogRawCommandPanel instance.

            :return: JogRawCommandPanel instance.
            :exceptions: None.
        '''
        return self._raw_panel

    def jog_step(self, axis: JogAxis | str, sign: float = 1.0) -> None:
        '''
            Sends relative jog command based on selected step size.

            :param axis: Axis identifier (JogAxis enum or str).
            :param sign: Direction multiplier (+1.0 or -1.0).
            :exceptions: None.
        '''
        self._axis_grid_panel.jog_step(axis, sign)

    def send_raw(self) -> None:
        '''
            Transmits raw command from text input to microcontroller.

            :exceptions: None.
        '''
        self._raw_panel.send_raw()
