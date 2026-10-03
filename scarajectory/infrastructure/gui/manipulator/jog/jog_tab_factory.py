# -*- coding: UTF-8 -*-

'''
Module
    jog_tab_factory.py
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

from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel import JogAxisGridPanel
from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel_factory import JogAxisGridPanelFactory
from scarajectory.infrastructure.gui.manipulator.jog.controllers_bundle import JogControllersBundle
from scarajectory.infrastructure.gui.manipulator.jog.panel_bundle import JogPanelBundle
from scarajectory.infrastructure.gui.manipulator.jog.power_panel import JogPowerPanel
from scarajectory.infrastructure.gui.manipulator.jog.power_panel_factory import JogPowerPanelFactory
from scarajectory.infrastructure.gui.manipulator.jog.raw_command_panel import JogRawCommandPanel
from scarajectory.infrastructure.gui.manipulator.jog.raw_command_panel_factory import JogRawCommandPanelFactory
from scarajectory.infrastructure.gui.manipulator.jog.jog_tab import JogTab
from scarajectory.infrastructure.gui.manipulator.jog.tool_panel import JogToolPanel
from scarajectory.infrastructure.gui.manipulator.jog.tool_panel_factory import JogToolPanelFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
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
        bundle: JogControllersBundle,
    ) -> JogTab:
        '''
            Instantiates and assembles a JogTab instance with sub-panels.

            :param parent: Parent container widget.
            :param bundle: Injected JogControllersBundle collaborator.
            :return: Configured and assembled JogTab instance.
            :exceptions: None.
        '''
        tab: JogTab = JogTab(parent)
        power_panel: JogPowerPanel = JogPowerPanelFactory.create(
            tab,
            motion_controller=bundle.motion_controller,
        )
        axis_grid_panel: JogAxisGridPanel = JogAxisGridPanelFactory.create(
            tab,
            jog_controller=bundle.jog_controller,
            query_controller=bundle.query_controller,
        )
        tool_panel: JogToolPanel = JogToolPanelFactory.create(
            tab,
            tool_controller=bundle.tool_controller,
        )
        raw_panel: JogRawCommandPanel = JogRawCommandPanelFactory.create(
            tab,
            raw_channel=bundle.raw_channel,
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
