# -*- coding: UTF-8 -*-

'''
Module
    canvas_mouse_handler_factory.py
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
    Factory service constructing CanvasMouseHandler instances with
    collaborator injection.
'''

from __future__ import annotations

from scaralang.core.service.trajectory.discretization.ishape_discretizer import IShapeDiscretizer
from scaralang.core.service.trajectory.discretization.shape_discretizer_factory import ShapeDiscretizerFactory
from scarajectory.infrastructure.gui.canvas.handler.canvas_drag_handler import CanvasDragHandler
from scarajectory.infrastructure.gui.canvas.handler.canvas_mouse_handler import CanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.canvas_shape_handler import CanvasShapeHandler
from scarajectory.infrastructure.gui.canvas.handler.mouse_handler_bundle import MouseHandlerBundle
from scarajectory.infrastructure.gui.canvas.handler.mouse_handler_init_bundle import MouseHandlerInitBundle
from scarajectory.infrastructure.gui.canvas.handler.pan.canvas_viewport_pan_handler import CanvasViewportPanHandler
from scarajectory.infrastructure.gui.canvas.handler.pan.canvas_viewport_pan_handler_factory import CanvasViewportPanHandlerFactory
from scarajectory.infrastructure.gui.canvas.handler.selection.canvas_selection_mouse_handler import CanvasSelectionMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.selection.canvas_selection_mouse_handler_factory import CanvasSelectionMouseHandlerFactory

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasMouseHandlerFactory:
    '''
        Factory providing creation of CanvasMouseHandler instances.

        It defines:

            :methods:
                | create - Constructs CanvasMouseHandler from collaborator bundle.
                | create_default - Constructs CanvasMouseHandler from init bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, bundle: MouseHandlerBundle) -> CanvasMouseHandler:
        '''
            Constructs CanvasMouseHandler with explicit collaborator bundle.

            :param bundle: Required MouseHandlerBundle container.
            :return: CanvasMouseHandler instance.
            :exceptions: None.
        '''
        return CanvasMouseHandler(bundle)

    @classmethod
    def create_default(
        cls,
        bundle: MouseHandlerInitBundle,
    ) -> CanvasMouseHandler:
        '''
            Constructs CanvasMouseHandler with default ShapeDiscretizer.

            :param bundle: Required MouseHandlerInitBundle container.
            :return: CanvasMouseHandler instance.
            :exceptions: None.
        '''
        discretizer: IShapeDiscretizer = ShapeDiscretizerFactory.create()
        shape_handler = CanvasShapeHandler(
            plan=bundle.mutation, discretizer=discretizer
        )
        drag_handler = CanvasDragHandler(
            store=bundle.store,
            mutation=bundle.mutation,
            state=bundle.state,
            shape_handler=shape_handler,
        )
        pan_handler: CanvasViewportPanHandler = (
            CanvasViewportPanHandlerFactory.create(
                vp=bundle.vp, state=bundle.state
            )
        )
        selection_handler: CanvasSelectionMouseHandler = (
            CanvasSelectionMouseHandlerFactory.create(
                store=bundle.store,
                selection=bundle.selection,
                mutation=bundle.mutation,
                vp=bundle.vp,
                state=bundle.state,
            )
        )
        handler_bundle = MouseHandlerBundle(
            vp=bundle.vp,
            state=bundle.state,
            pan_handler=pan_handler,
            selection_handler=selection_handler,
            shape_handler=shape_handler,
            drag_handler=drag_handler,
        )

        return cls.create(handler_bundle)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
