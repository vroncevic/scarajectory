# -*- coding: UTF-8 -*-

'''
Module
    icanvas.py
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
    Defines interface ICanvas for vector CAD canvas components.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.infrastructure.gui.model.canvas_settings import CanvasSettings
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICanvas(Protocol):
    '''
        Contract for vector CAD canvas operations.

        It defines:

            :methods:
                | set_tool_mode - Sets the active drawing/selection tool mode.
                | update_settings - Updates default point properties.
    '''

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Sets the active drawing/selection tool mode.

            :param mode: CanvasToolMode enum.
        '''

    def update_settings(self, settings: CanvasSettings) -> None:
        '''
            Updates default point properties.

            :param settings: CanvasSettings instance.
        '''
