# -*- coding: UTF-8 -*-

'''
Module
    iassembler.py
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
    Protocol defining toolbar section assembly interface.
'''

from __future__ import annotations

from tkinter import Widget
from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.toolbar.bundle import ToolbarBundle
from scarajectory.infrastructure.gui.toolbar.section.bundle import SectionsBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ISectionsAssembler(Protocol):
    '''
        Protocol defining toolbar section assembly interface.

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
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Version string.
        '''
