# -*- coding: UTF-8 -*-

'''
Module
    toolbar.py
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
    Top toolbar housing CAD drawing tools, zoom controls, plan undo/redo
    and default settings.
'''

from __future__ import annotations

from tkinter import Widget
from tkinter.ttk import Frame
from typing import Final

from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle
from scarajectory.infrastructure.gui.toolbar.section.iassembler import ISectionsAssembler

__author__ = 'Vladimir Roncevic'
__copyright__ = 'Copyright (C) 2026 Vladimir Roncevic <elektron.ronca@gmail.com>'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Toolbar(Frame):
    '''
        Application toolbar for mode selection, CAD actions, and kinematic
        defaults.

        It defines:

            :attributes:
                | _sections - Container holding mounted toolbar sub-sections.
            :methods:
                | __init__ - Initializes toolbar container and mounts sections.
                | set_deadzone - Sets deadzone enforcement checkbox state.
                | get_version - Returns component version string.
    '''

    def __init__(
        self,
        parent: Widget,
        assembler: ISectionsAssembler,
        bundle: ToolbarBundle,
    ) -> None:
        '''
            Initializes toolbar container and mounts sections.

            :param parent: Parent container widget.
            :param assembler: Section assembler interface.
            :param bundle: Toolbar dependency and parameters bundle.
            :exceptions: None.
        '''
        super().__init__(parent, padding=(8, 6))
        self._sections: Final[SectionsBundle] = assembler.assemble_sections(
            self, bundle
        )

    def set_deadzone(self, enabled: bool) -> None:
        '''
            Sets deadzone enforcement checkbox state.

            :param enabled: True to enforce deadzone, False to disable.
            :exceptions: None.
        '''
        self._sections.param_section.set_deadzone(enabled)

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
