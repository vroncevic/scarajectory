# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory providing JogTab instances.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.manipulator.jog.dependencies import JogDependencies
from scarajectory.infrastructure.gui.manipulator.jog.panel.axis_grid import JogAxisGridPanel
from scarajectory.infrastructure.gui.manipulator.jog.panel.bundle import JogPanelBundle
from scarajectory.infrastructure.gui.manipulator.jog.panel.power import JogPowerPanel
from scarajectory.infrastructure.gui.manipulator.jog.panel.raw_command import JogRawCommandPanel
from scarajectory.infrastructure.gui.manipulator.jog.panel.tool import JogToolPanel
from scarajectory.infrastructure.gui.manipulator.jog.tab import JogTab

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class JogTabFactory:
    '''
        Factory providing JogTab instances.

        It defines:

            :methods:
                | create - Instantiates and assembles a JogTab instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        dependencies: JogDependencies,
    ) -> JogTab:
        '''
            Instantiates and assembles a JogTab instance with sub-panels.

            :param parent: Parent container widget.
            :param dependencies: Injected JogDependencies collaborator.
            :return: Configured and assembled JogTab instance.
            :exceptions: None.
        '''
        tab: JogTab = JogTab(parent)
        power_panel: JogPowerPanel = JogPowerPanel(
            tab,
            motion_controller=dependencies.motion_controller,
        )
        axis_grid_panel: JogAxisGridPanel = JogAxisGridPanel(
            tab,
            jog_controller=dependencies.jog_controller,
            query_controller=dependencies.query_controller,
        )
        tool_panel: JogToolPanel = JogToolPanel(
            tab,
            tool_controller=dependencies.tool_controller,
        )
        raw_panel: JogRawCommandPanel = JogRawCommandPanel(
            tab,
            raw_channel=dependencies.raw_channel,
        )
        panels: JogPanelBundle = JogPanelBundle(
            power_panel=power_panel,
            axis_grid_panel=axis_grid_panel,
            tool_panel=tool_panel,
            raw_panel=raw_panel,
        )
        tab.mount_panels(panels)

        return tab

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns the factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
