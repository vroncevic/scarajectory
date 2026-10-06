# -*- coding: UTF-8 -*-

'''
Module
    trajectory_canvas_factory.py
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
    Factory service assembling TrajectoryCanvas with full collaborator graph.
'''

from __future__ import annotations

from tkinter import Widget

from scarajectory.infrastructure.gui.canvas.bundle import CanvasBundle
from scarajectory.infrastructure.gui.canvas.canvas_event_binder import CanvasEventBinder
from scarajectory.infrastructure.gui.canvas.canvas_event_binder_factory import CanvasEventBinderFactory
from scarajectory.infrastructure.gui.canvas.observer.canvas_plan_observer_bridge import CanvasPlanObserverBridge
from scarajectory.infrastructure.gui.canvas.observer.canvas_plan_observer_bridge_factory import CanvasPlanObserverBridgeFactory
from scarajectory.infrastructure.gui.canvas.status.canvas_status_presenter import CanvasStatusPresenter
from scarajectory.infrastructure.gui.canvas.status.canvas_status_presenter_factory import CanvasStatusPresenterFactory
from scarajectory.infrastructure.gui.canvas.navigation.canvas_view_navigator import CanvasViewNavigator
from scarajectory.infrastructure.gui.canvas.navigation.canvas_view_navigator_factory import CanvasViewNavigatorFactory
from scarajectory.infrastructure.gui.canvas.handler.canvas_mouse_handler import CanvasMouseHandler
from scarajectory.infrastructure.gui.canvas.handler.canvas_mouse_handler_factory import CanvasMouseHandlerFactory
from scarajectory.infrastructure.gui.canvas.handler.mouse_handler_init_bundle import MouseHandlerInitBundle
from scarajectory.infrastructure.gui.canvas.trajectory_canvas import TrajectoryCanvas
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


class TrajectoryCanvasFactory:
    '''
        Factory providing instantiation and wiring of TrajectoryCanvas components.

        It defines:

            :methods:
                | create - Constructs and wires a TrajectoryCanvas instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        parent: Widget,
        *,
        bundle: CanvasBundle,
    ) -> TrajectoryCanvas:
        '''
            Constructs and wires a TrajectoryCanvas instance with collaborators.

            :param parent: Parent Tk widget container.
            :param bundle: Required CanvasBundle dependency container.
            :return: Fully assembled TrajectoryCanvas instance.
            :exceptions: None.
        '''
        vp = ViewportTransform()
        state = CanvasInteractionState()
        mouse_init_bundle = MouseHandlerInitBundle(
            store=bundle.store,
            selection=bundle.selection,
            mutation=bundle.mutation,
            vp=vp,
            state=state,
        )
        mouse_handler: CanvasMouseHandler = (
            CanvasMouseHandlerFactory.create_default(mouse_init_bundle)
        )
        canvas = TrajectoryCanvas(parent, bundle=bundle, vp=vp, state=state)
        navigator: CanvasViewNavigator = CanvasViewNavigatorFactory.create(
            viewport=vp, validator=bundle.validator, target=canvas
        )
        status_presenter: CanvasStatusPresenter = (
            CanvasStatusPresenterFactory.create()
        )
        canvas.attach_presentation(navigator, status_presenter)
        observer_bridge: CanvasPlanObserverBridge = (
            CanvasPlanObserverBridgeFactory.create(canvas.redraw)
        )
        bundle.dispatcher.add_observer(observer_bridge)

        event_binder: CanvasEventBinder = CanvasEventBinderFactory.create(
            canvas,
            mouse_handler=mouse_handler,
            navigator=navigator,
            status_presenter=status_presenter,
        )
        event_binder.bind_events()

        return canvas

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
