# -*- coding: UTF-8 -*-

'''
Module
    canvas_tool_mode.py
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
    Defines CanvasToolMode enumeration for vector canvas editing tools.
'''

from __future__ import annotations

from enum import Enum, auto

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasToolMode(Enum):
    '''
        Active interaction mode on the CAD canvas.

        It defines:

            :attributes:
                | SELECT - Select and move existing waypoints.
                | POINT - Click to append discrete waypoints.
                | CIRCLE - Click and drag to create circular patterns.
                | RECTANGLE - Click and drag to create rectangular paths.
                | FREEHAND - Drag to stream freeform continuous paths.
    '''

    SELECT = auto()
    POINT = auto()
    CIRCLE = auto()
    RECTANGLE = auto()
    FREEHAND = auto()
