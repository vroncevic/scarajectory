# -*- coding: UTF-8 -*-

'''
Module
    canvas_selection_mouse_handler_factory.py
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
    Factory service constructing CanvasSelectionMouseHandler instances.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.plan.mutation.iplan_point_mutator import IPlanPointMutator
from scarajectory.core.service.trajectory.plan.selection.iplan_selection_coordinator import IPlanSelectionCoordinator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.canvas.handler.selection.canvas_selection_mouse_handler import CanvasSelectionMouseHandler
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


class CanvasSelectionMouseHandlerFactory:
    '''
        Factory providing creation of CanvasSelectionMouseHandler instances.

        It defines:

            :methods:
                | create - Constructs handler with injected dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        store: IWaypointStore,
        selection: IPlanSelectionCoordinator,
        mutation: IPlanPointMutator,
        vp: ViewportTransform,
        state: CanvasInteractionState,
    ) -> CanvasSelectionMouseHandler:
        '''
            Constructs CanvasSelectionMouseHandler with injected dependencies.

            :param store: Injected IWaypointStore instance.
            :param selection: Injected IPlanSelectionCoordinator instance.
            :param mutation: Injected IPlanPointMutator instance.
            :param vp: Injected ViewportTransform instance.
            :param state: Injected CanvasInteractionState instance.
            :return: CanvasSelectionMouseHandler instance.
            :exceptions: None.
        '''
        return CanvasSelectionMouseHandler(
            store=store,
            selection=selection,
            mutation=mutation,
            vp=vp,
            state=state,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
