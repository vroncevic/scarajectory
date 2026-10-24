# -*- coding: UTF-8 -*-

'''
Module
    assembler.py
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
    Assembler service coordinating instantiation and layout of toolbar sections.
'''

from __future__ import annotations

from tkinter import LEFT, RIGHT, VERTICAL, Widget, X, Y
from tkinter.ttk import Separator

from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle
from scarajectory.infrastructure.gui.toolbar.section.navigation import NavigationSection
from scarajectory.infrastructure.gui.toolbar.section.parameter import ParameterSection
from scarajectory.infrastructure.gui.toolbar.section.status import StatusSection
from scarajectory.infrastructure.gui.toolbar.section.tool import ToolSection

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class SectionsAssembler:
    '''
        Assembler service coordinating instantiation and layout of toolbar sections.

        It defines:

            :methods:
                | assemble_sections - Assembles toolbar sections into SectionsBundle.
                | get_version - Returns component version string.
    '''

    def assemble_sections(
        self,
        parent: Widget,
        bundle: ToolbarBundle,
    ) -> SectionsBundle:
        '''
            Assembles toolbar sections into SectionsBundle.

            :param parent: Parent container widget.
            :param bundle: Toolbar bundle.
            :return: Sections bundle.
            :exceptions: None.
        '''
        tool_section: ToolSection = ToolSection(parent, bundle.canvas)
        nav_section: NavigationSection = NavigationSection(
            parent, bundle.navigator, bundle.history
        )
        param_section: ParameterSection = ParameterSection(
            parent,
            canvas=bundle.canvas,
            reach_limits=(bundle.r_min, bundle.r_max),
            settings=bundle.settings,
        )
        status_section: StatusSection = StatusSection(
            parent, bundle.status_presenter
        )

        tool_section.pack(side=LEFT)
        Separator(parent, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)

        nav_section.pack(side=LEFT)
        Separator(parent, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=8)

        status_section.pack(side=RIGHT, padx=4)
        param_section.pack(side=LEFT, fill=X, expand=True)

        return SectionsBundle(
            tool_section=tool_section,
            nav_section=nav_section,
            param_section=param_section,
            status_section=status_section,
        )

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
