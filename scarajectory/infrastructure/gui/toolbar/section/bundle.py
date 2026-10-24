# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Container bundle holding instantiated toolbar sub-sections.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.gui.toolbar.section.navigation import NavigationSection
from scarajectory.infrastructure.gui.toolbar.section.parameter import ParameterSection
from scarajectory.infrastructure.gui.toolbar.section.status import StatusSection
from scarajectory.infrastructure.gui.toolbar.section.tool import ToolSection

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class SectionsBundle:
    '''
        Immutable data container holding the toolbar sub-sections.

        It defines:

            :attributes:
                | tool_section - CAD drawing tool mode selector subcomponent.
                | nav_section - Viewport navigation and history controls subcomponent.
                | param_section - Waypoint parameter inputs and reach limit subcomponent.
                | status_section - Live cursor telemetry and zoom level subcomponent.
    '''

    tool_section: ToolSection
    nav_section: NavigationSection
    param_section: ParameterSection
    status_section: StatusSection
