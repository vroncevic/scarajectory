# -*- coding: UTF-8 -*-

'''
Module
    canvas_view_navigator.py
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
    Coordinates viewport camera scaling, centering, and workspace reach fitting.
'''

from __future__ import annotations

from typing import Final

from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_target import ICanvasViewTarget
from scarajectory.infrastructure.gui.model.viewport_transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewNavigator:
    '''
        Coordinates viewport camera scaling, centering, and workspace reach fitting.

        It defines:

            :attributes:
                | _viewport - Viewport transformation matrix.
                | _validator - Kinematic reachability validator.
                | _target - Canvas rendering and dimension query target.
            :methods:
                | __init__ - Initializes canvas view navigator with collaborators.
                | fit_reach_view - Fits maximum reach circle into viewport.
                | reset_view - Resets viewport zoom to 100% and centers workspace.
                | zoom_in - Scales viewport view in by zoom factor.
                | zoom_out - Scales viewport view out by zoom factor.
    '''

    _viewport: ViewportTransform
    _validator: ITrajectoryValidator
    _target: ICanvasViewTarget

    def __init__(
        self,
        viewport: ViewportTransform,
        validator: ITrajectoryValidator,
        target: ICanvasViewTarget,
    ) -> None:
        '''
            Initializes canvas view navigator with collaborators.

            :param viewport: ViewportTransform instance.
            :param validator: ITrajectoryValidator instance.
            :param target: ICanvasViewTarget instance.
            :exceptions: None.
        '''
        self._viewport: Final[ViewportTransform] = viewport
        self._validator: Final[ITrajectoryValidator] = validator
        self._target: Final[ICanvasViewTarget] = target

    def fit_reach_view(self) -> None:
        '''
            Fits maximum reach circle into viewport and redraws scene.

            :exceptions: None.
        '''
        w, h = self._target.get_view_dimensions()
        self._viewport.fit_reach(w, h, self._validator.r_max)
        self._target.redraw()

    def reset_view(self) -> None:
        '''
            Resets viewport zoom to 100%, centers workspace, and redraws scene.

            :exceptions: None.
        '''
        self._viewport.reset()
        self._target.redraw()

    def zoom_in(self) -> None:
        '''
            Scales viewport view in by zoom factor and redraws scene.

            :exceptions: None.
        '''
        self._viewport.zoom_in()
        self._target.redraw()

    def zoom_out(self) -> None:
        '''
            Scales viewport view out by zoom factor and redraws scene.

            :exceptions: None.
        '''
        self._viewport.zoom_out()
        self._target.redraw()
