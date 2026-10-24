# -*- coding: UTF-8 -*-

'''
Module
    handler.py
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
    Resize event handler adjusting Treeview column widths proportionally.
'''

from __future__ import annotations

from tkinter.ttk import Treeview
from types import MappingProxyType
from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TableResizeHandler:
    '''
        Handles proportional resizing of Treeview columns based on container width.

        It defines:

            :constants:
                | COL_RATIOS - Proportional width ratios per column.
                | MIN_WIDTHS - Minimum threshold width per column in pixels.
                | OFFSET_WIDTH - Horizontal layout margin subtracted from container width.
                | MIN_TOTAL_WIDTH - Minimum effective table width boundary.
                | ATTR_WIDTH - Name of width attribute on configure event object.
                | DEFAULT_WIDTH - Fallback width when attribute is missing.
            :methods:
                | handle_resize - Adjusts table column widths proportionally on container resize.
                | get_version - Returns handler version string.
    '''

    COL_RATIOS: ClassVar[MappingProxyType[str, float]] = MappingProxyType({
        'idx': 0.08,
        'x': 0.15,
        'y': 0.15,
        'z': 0.14,
        'phi': 0.15,
        'speed': 0.17,
        'reach': 0.16,
    })

    MIN_WIDTHS: ClassVar[MappingProxyType[str, int]] = MappingProxyType({
        'idx': 35,
        'x': 65,
        'y': 65,
        'z': 60,
        'phi': 65,
        'speed': 85,
        'reach': 75,
    })

    OFFSET_WIDTH: ClassVar[int] = 24
    MIN_TOTAL_WIDTH: ClassVar[int] = 450
    ATTR_WIDTH: ClassVar[str] = 'width'
    DEFAULT_WIDTH: ClassVar[int] = 0

    def handle_resize(self, tree: Treeview, event: object) -> None:
        '''
            Adjusts table column widths proportionally on container resize.

            :param tree: Target Treeview widget.
            :param event: Tkinter configure event.
            :exceptions: None.
        '''
        width: int = getattr(event, self.ATTR_WIDTH, self.DEFAULT_WIDTH)
        if width <= self.DEFAULT_WIDTH:
            return

        total_w: int = max(width - self.OFFSET_WIDTH, self.MIN_TOTAL_WIDTH)
        for col_id, ratio in self.COL_RATIOS.items():
            col_w: int = max(self.MIN_WIDTHS[col_id], int(total_w * ratio))
            tree.column(col_id, width=col_w)

    def get_version(self) -> str:
        '''
            Returns handler version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
