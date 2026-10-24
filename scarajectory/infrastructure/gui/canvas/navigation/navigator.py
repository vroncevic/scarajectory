# -*- coding: UTF-8 -*-

'''
Module
    navigator.py
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
    Coordinates canvas view zooming, resetting, and workspace reach fitting.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.validation.ivalidator import ITrajectoryValidator
from scarajectory.infrastructure.gui.canvas.navigation.itarget import ICanvasViewTarget
from scarajectory.infrastructure.gui.canvas.transform.icamera import IViewportCamera

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewNavigator:
    '''
        Coordinates canvas view zooming, resetting, and workspace reach fitting.

        It defines:

            :attributes:
                | _camera - Injected viewport camera controller.
                | _validator - Injected trajectory kinematic validator.
                | _target - Injected canvas view target for dimensions and redraws.
            :methods:
                | __init__ - Initializes canvas view navigator with collaborators.
                | fit_reach_view - Fits maximum reach circle into viewport.
                | reset_view - Resets viewport zoom to 100% and centers workspace.
                | zoom_in - Scales viewport view in by zoom factor.
                | zoom_out - Scales viewport view out by zoom factor.
    '''

    _camera: IViewportCamera
    _validator: ITrajectoryValidator
    _target: ICanvasViewTarget

    def __init__(
        self,
        camera: IViewportCamera,
        validator: ITrajectoryValidator,
        target: ICanvasViewTarget,
    ) -> None:
        '''
            Initializes canvas view navigator with collaborators.

            :param camera: IViewportCamera instance.
            :param validator: ITrajectoryValidator instance.
            :param target: ICanvasViewTarget instance.
            :exceptions: None.
        '''
        self._camera: Final[IViewportCamera] = camera
        self._validator: Final[ITrajectoryValidator] = validator
        self._target: Final[ICanvasViewTarget] = target

    def fit_reach_view(self) -> None:
        '''
            Fits maximum reach circle into viewport and redraws scene.

            :exceptions: None.
        '''
        w, h = self._target.get_view_dimensions()
        self._camera.fit_reach(w, h, self._validator.r_max)
        self._target.redraw()

    def reset_view(self) -> None:
        '''
            Resets viewport zoom to 100%, centers workspace, and redraws scene.

            :exceptions: None.
        '''
        self._camera.reset()
        self._target.redraw()

    def zoom_in(self) -> None:
        '''
            Scales viewport view in by zoom factor and redraws scene.

            :exceptions: None.
        '''
        self._camera.zoom_in()
        self._target.redraw()

    def zoom_out(self) -> None:
        '''
            Scales viewport view out by zoom factor and redraws scene.

            :exceptions: None.
        '''
        self._camera.zoom_out()
        self._target.redraw()
