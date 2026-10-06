# -*- coding: UTF-8 -*-

'''
Module
    panel_bundle.py
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
    Parameter bundle holding assembled sub-panels for JogTab composition.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.gui.manipulator.jog.axis_grid_panel import JogAxisGridPanel
from scarajectory.infrastructure.gui.manipulator.jog.power_panel import JogPowerPanel
from scarajectory.infrastructure.gui.manipulator.jog.raw_command_panel import JogRawCommandPanel
from scarajectory.infrastructure.gui.manipulator.jog.tool_panel import JogToolPanel

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class JogPanelBundle:
    '''
        Bundle containing assembled sub-panels for JogTab.

        It defines:

            :attributes:
                | power_panel - Sub-panel for power and homing commands.
                | axis_grid_panel - Sub-panel for directional jog steps and step size.
                | tool_panel - Sub-panel for pneumatic pump and purge valve toggles.
                | raw_panel - Sub-panel for raw ASCII micro-command transmission.
    '''

    power_panel: JogPowerPanel
    axis_grid_panel: JogAxisGridPanel
    tool_panel: JogToolPanel
    raw_panel: JogRawCommandPanel
