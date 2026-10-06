# -*- coding: UTF-8 -*-

'''
Module
    canvas_viewport_pan_handler_factory.py
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
    Factory service constructing CanvasViewportPanHandler instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.canvas.handler.pan.canvas_viewport_pan_handler import CanvasViewportPanHandler
from scarajectory.infrastructure.gui.model.canvas_interaction_state import CanvasInteractionState
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewportPanHandlerFactory:
    '''
        Factory providing creation of CanvasViewportPanHandler instances.

        It defines:

            :methods:
                | create - Constructs handler with viewport and state.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        vp: ViewportTransform,
        state: CanvasInteractionState,
    ) -> CanvasViewportPanHandler:
        '''
            Constructs CanvasViewportPanHandler with viewport and state.

            :param vp: Required ViewportTransform instance.
            :param state: Required CanvasInteractionState instance.
            :return: CanvasViewportPanHandler instance.
            :exceptions: None.
        '''
        return CanvasViewportPanHandler(vp=vp, state=state)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
