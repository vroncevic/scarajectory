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
    Defines abstract interface ICanvas for vector CAD canvas components.
'''

from __future__ import annotations

from abc import ABC, abstractmethod

from scarajectory.core.model.canvas_tool_mode import CanvasToolMode
from scarajectory.core.model.canvas_settings_dto import CanvasSettingsDTO

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ICanvas(ABC):
    '''
        Abstract contract for vector CAD canvas operations.

        It defines:

            :methods:
                | set_tool_mode - Sets the active drawing/selection tool mode.
                | update_settings - Updates default point properties.
                | zoom_in - Scales canvas view in by 1.25x.
                | zoom_out - Scales canvas view out by 0.8x.
                | reset_view - Resets viewport zoom to 100%.
                | fit_reach_view - Fits maximum reach circle to canvas view.
    '''

    @abstractmethod
    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Sets the active drawing/selection tool mode.

            :param mode: CanvasToolMode enum.
            :exceptions: None.
        '''

    @abstractmethod
    def update_settings(self, settings: CanvasSettingsDTO) -> None:
        '''
            Updates default point properties.

            :param settings: CanvasSettingsDTO instance.
            :exceptions: None.
        '''

    @abstractmethod
    def zoom_in(self) -> None:
        '''
            Scales canvas view in by 1.25x.

            :exceptions: None.
        '''

    @abstractmethod
    def zoom_out(self) -> None:
        '''
            Scales canvas view out by 0.8x.

            :exceptions: None.
        '''

    @abstractmethod
    def reset_view(self) -> None:
        '''
            Resets viewport zoom to 100%.

            :exceptions: None.
        '''

    @abstractmethod
    def fit_reach_view(self) -> None:
        '''
            Fits maximum reach circle to canvas view.

            :exceptions: None.
        '''
