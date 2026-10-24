# -*- coding: UTF-8 -*-

'''
Module
    camera.py
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
    Manages viewport camera zooming, scaling, and framing operations.
'''

from __future__ import annotations

from typing import ClassVar, Final

from scarajectory.infrastructure.gui.canvas.transform.transform import ViewportTransform

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ViewportCamera:
    '''
        Manages viewport camera zooming, scaling, and framing controls.

        It defines:

            :attributes:
                | DEFAULT_ZOOM - Default initial zoom factor.
                | ZOOM_IN_FACTOR - Scale multiplier for zoom in operation.
                | ZOOM_OUT_FACTOR - Scale multiplier for zoom out operation.
                | ZOOM_MIN - Minimum allowable zoom scale.
                | ZOOM_MAX - Maximum allowable zoom scale.
                | REACH_COVERAGE_RATIO - Fraction of viewport dimension used for fit reach view.
                | MIN_CANVAS_DIMENSION - Minimum canvas dimension threshold for fit reach.
                | _transform - Injected ViewportTransform state carrier.
            :methods:
                | __init__ - Initializes camera with viewport transform state.
                | zoom_in - Increases zoom scale by factor.
                | zoom_out - Decreases zoom scale by factor.
                | reset - Resets scale and pan offset to defaults.
                | fit_reach - Adjusts scale and pan to fit robot reach boundary into window.
    '''

    DEFAULT_ZOOM: ClassVar[float] = 1.35
    ZOOM_IN_FACTOR: ClassVar[float] = 1.25
    ZOOM_OUT_FACTOR: ClassVar[float] = 0.8
    ZOOM_MIN: ClassVar[float] = 0.3
    ZOOM_MAX: ClassVar[float] = 5.0
    REACH_COVERAGE_RATIO: ClassVar[float] = 0.45
    MIN_CANVAS_DIMENSION: ClassVar[int] = 20

    _transform: ViewportTransform

    def __init__(self, transform: ViewportTransform) -> None:
        '''
            Initializes camera with viewport transform state.

            :param transform: ViewportTransform state carrier.
            :exceptions: None.
        '''
        self._transform: Final[ViewportTransform] = transform

    def zoom_in(self) -> None:
        '''
            Increases zoom scale by factor.

            :exceptions: None.
        '''
        self._transform.scale = min(
            self.ZOOM_MAX, self._transform.scale * self.ZOOM_IN_FACTOR
        )

    def zoom_out(self) -> None:
        '''
            Decreases zoom scale by factor.

            :exceptions: None.
        '''
        self._transform.scale = max(
            self.ZOOM_MIN, self._transform.scale * self.ZOOM_OUT_FACTOR
        )

    def reset(self) -> None:
        '''
            Resets scale and pan offset to defaults.

            :exceptions: None.
        '''
        self._transform.scale = self.DEFAULT_ZOOM
        self._transform.pan_x = 0.0
        self._transform.pan_y = 0.0

    def fit_reach(
        self,
        width: int,
        height: int,
        r_max_mm: float,
    ) -> None:
        '''
            Adjusts scale and pan to fit robot reach boundary into window.

            :param width: Canvas width in pixels.
            :param height: Canvas height in pixels.
            :param r_max_mm: Maximum robot reach in mm.
            :exceptions: None.
        '''
        if width > self.MIN_CANVAS_DIMENSION and height > self.MIN_CANVAS_DIMENSION:
            min_dim: float = float(min(width, height))
            self._transform.scale = (min_dim * self.REACH_COVERAGE_RATIO) / r_max_mm
            self._transform.pan_x = 0.0
            self._transform.pan_y = 0.0
