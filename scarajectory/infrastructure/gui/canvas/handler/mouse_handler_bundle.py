# -*- coding: UTF-8 -*-

'''
Module
    mouse_handler_bundle.py
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
    Parameter bundle for CanvasMouseHandler collaborators.
'''

from __future__ import annotations

from dataclasses import dataclass

from scarajectory.infrastructure.gui.canvas.handler.canvas_drag_handler import CanvasDragHandler
from scarajectory.infrastructure.gui.canvas.handler.canvas_shape_handler import CanvasShapeHandler
from scarajectory.infrastructure.gui.canvas.handler.pan.icanvas_viewport_pan_handler import ICanvasViewportPanHandler
from scarajectory.infrastructure.gui.canvas.handler.selection.icanvas_selection_mouse_handler import ICanvasSelectionMouseHandler
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(frozen=True)
class MouseHandlerBundle:
    '''
        Immutable container holding collaborators for CanvasMouseHandler.

        It defines:

            :attributes:
                | vp - Viewport transformation matrix.
                | state - Interactive mouse pan, drag and selection state.
                | pan_handler - Injected pan handler interface.
                | selection_handler - Injected selection handler interface.
                | shape_handler - Injected shape creation handler.
                | drag_handler - Injected drag motion handler.
    '''

    vp: ViewportTransform
    state: CanvasInteractionState
    pan_handler: ICanvasViewportPanHandler
    selection_handler: ICanvasSelectionMouseHandler
    shape_handler: CanvasShapeHandler
    drag_handler: CanvasDragHandler
