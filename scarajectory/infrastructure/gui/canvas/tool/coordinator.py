# -*- coding: UTF-8 -*-

'''
Module
    coordinator.py
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
    Coordinates active canvas tool mode and drag interaction state.
'''

from __future__ import annotations

from typing import Final

from scarajectory.infrastructure.gui.canvas.handler.state import CanvasInteractionState
from scarajectory.infrastructure.gui.canvas.observer.iredraw_delegate import ICanvasRedrawDelegate
from scarajectory.infrastructure.gui.model.canvas_tool_mode import CanvasToolMode

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasToolModeCoordinator:
    '''
        Coordinates active canvas tool mode and drag interaction state.

        It defines:

            :attributes:
                | _state - Interactive mouse pan, drag and selection state.
                | _redraw_delegate - Delegate to trigger canvas redraw.
                | _tool_mode - Active interactive drawing tool mode.
            :methods:
                | __init__ - Initializes the tool mode coordinator.
                | set_tool_mode - Changes active drawing/selection tool.
                | reset - Resets tool mode to default POINT mode.
                | tool_mode - Returns active drawing or selection tool mode.
    '''

    _state: CanvasInteractionState
    _redraw_delegate: ICanvasRedrawDelegate
    _tool_mode: CanvasToolMode

    def __init__(
        self,
        state: CanvasInteractionState,
        redraw_delegate: ICanvasRedrawDelegate,
    ) -> None:
        '''
            Initializes the tool mode coordinator.

            :param state: Required CanvasInteractionState instance.
            :param redraw_delegate: Required ICanvasRedrawDelegate collaborator.
            :exceptions: None.
        '''
        self._state: Final[CanvasInteractionState] = state
        self._redraw_delegate: Final[ICanvasRedrawDelegate] = redraw_delegate
        self._tool_mode = CanvasToolMode.POINT

    def set_tool_mode(self, mode: CanvasToolMode) -> None:
        '''
            Changes active drawing/selection tool and triggers redraw.

            :param mode: CanvasToolMode enum value.
            :exceptions: None.
        '''
        self._tool_mode = mode
        self._state.reset_drag()
        self._redraw_delegate.redraw()

    def reset(self) -> None:
        '''
            Resets tool mode to default POINT mode.

            :exceptions: None.
        '''
        self.set_tool_mode(CanvasToolMode.POINT)

    @property
    def tool_mode(self) -> CanvasToolMode:
        '''
            Returns active drawing or selection tool mode.

            :return: CanvasToolMode enum value.
            :exceptions: None.
        '''
        return self._tool_mode
