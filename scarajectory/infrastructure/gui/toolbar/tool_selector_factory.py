# -*- coding: UTF-8 -*-

'''
Module
    tool_selector_factory.py
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
    Factory for instantiating ToolbarToolSelector components.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.canvas.icanvas import ICanvas
from scarajectory.infrastructure.gui.toolbar.tool_selector import ToolbarToolSelector

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolbarToolSelectorFactory:
    '''
        Factory responsible for creating ToolbarToolSelector instances.

        It defines:

            :methods:
                | create - Creates a ToolbarToolSelector widget instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        canvas: ICanvas,
    ) -> ToolbarToolSelector:
        '''
            Creates a ToolbarToolSelector widget instance.

            :param parent: Parent container widget.
            :param canvas: Active CAD canvas interface.
            :return: Fully configured ToolbarToolSelector instance.
            :exceptions: None.
        '''
        return ToolbarToolSelector(parent, canvas)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
