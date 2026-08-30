# -*- coding: UTF-8 -*-

'''
Module
    canvas_interaction_state.py
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
    Encapsulates interactive CAD canvas mouse drag, pan and selection state.
'''

from __future__ import annotations

from dataclasses import dataclass

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True)
class CanvasInteractionState:
    '''
        Encapsulates interactive CAD canvas mouse drag, pan and selection state.

        It defines:

            :attributes:
                | pan_x - Viewport panning origin coordinate X in pixels.
                | pan_y - Viewport panning origin coordinate Y in pixels.
                | is_panning - Viewport panning active flag.
                | drag_start_world - Drag start point in world coordinate space (x, y) mm.
                | drag_current_world - Active cursor drag position in world coordinate space (x, y) mm.
                | dragged_node_idx - Index of selected waypoint being dragged, or -1 if none.
            :methods:
                | reset_drag - Clears active drag coordinates and node index.
                | reset_pan - Clears panning state and coordinates.
    '''

    pan_x: int = 0
    pan_y: int = 0
    is_panning: bool = False
    drag_start_world: tuple[float, float] | None = None
    drag_current_world: tuple[float, float] | None = None
    dragged_node_idx: int = -1

    def reset_drag(self) -> None:
        '''
            Clears active drag coordinates and node index.

            :exceptions: None.
        '''
        self.drag_start_world = None
        self.drag_current_world = None
        self.dragged_node_idx = -1

    def reset_pan(self) -> None:
        '''
            Clears panning state and coordinates.

            :exceptions: None.
        '''
        self.pan_x = 0
        self.pan_y = 0
        self.is_panning = False
