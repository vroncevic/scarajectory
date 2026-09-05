# -*- coding: UTF-8 -*-

'''
Module
    viewport_transform.py
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
    Manages 2D viewport coordinates, zoom scale and pan offset transformations.
'''

from __future__ import annotations

from typing import ClassVar

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ViewportTransform:
    '''
        Manages 2D viewport coordinate transformations between millimeters and screen pixels.

        It defines:

            :attributes:
                | DEFAULT_ZOOM - Default initial zoom factor.
                | R_MAX_MM - Maximum robot reach in millimeters.
                | ZOOM_IN_FACTOR - Scale multiplier for zoom in operation.
                | ZOOM_OUT_FACTOR - Scale multiplier for zoom out operation.
                | ZOOM_MIN - Minimum allowable zoom scale.
                | ZOOM_MAX - Maximum allowable zoom scale.
                | REACH_COVERAGE_RATIO - Fraction of viewport dimension used for fit reach view.
                | MIN_CANVAS_DIMENSION - Minimum canvas dimension threshold for fit reach.
                | scale - Active zoom scale.
                | pan_x - Horizontal pan offset in pixels.
                | pan_y - Vertical pan offset in pixels.
            :methods:
                | __init__ - Initializes default zoom scale and zero pan offset.
                | world_to_screen - Converts world mm coordinates to canvas screen pixels.
                | screen_to_world - Converts screen pixels to world mm coordinates.
                | zoom_in - Increases zoom scale by factor.
                | zoom_out - Decreases zoom scale by factor.
                | reset - Resets scale and pan offset to defaults.
                | fit_reach - Adjusts scale and pan to fit robot reach boundary into window.
    '''

    DEFAULT_ZOOM: ClassVar[float] = 1.35
    R_MAX_MM: ClassVar[float] = 270.0
    ZOOM_IN_FACTOR: ClassVar[float] = 1.25
    ZOOM_OUT_FACTOR: ClassVar[float] = 0.8
    ZOOM_MIN: ClassVar[float] = 0.3
    ZOOM_MAX: ClassVar[float] = 5.0
    REACH_COVERAGE_RATIO: ClassVar[float] = 0.45
    MIN_CANVAS_DIMENSION: ClassVar[int] = 20

    scale: float
    pan_x: float
    pan_y: float

    def __init__(self) -> None:
        '''
            Initializes default zoom scale and zero pan offset.

            :exceptions: None.
        '''
        self.scale = self.DEFAULT_ZOOM
        self.pan_x = 0.0
        self.pan_y = 0.0

    def world_to_screen(self, x: float, y: float, width: int, height: int) -> tuple[float, float]:
        '''
            Converts world mm coordinates to canvas screen pixels.

            :param x: World X coordinate in mm.
            :param y: World Y coordinate in mm.
            :param width: Canvas pixel width.
            :param height: Canvas pixel height.
            :return: Tuple of screen (sx, sy) pixel coordinates.
            :exceptions: None.
        '''
        cx: float = width / 2.0 + self.pan_x
        cy: float = height / 2.0 + self.pan_y
        return (cx + x * self.scale, cy - y * self.scale)

    def screen_to_world(self, sx: float, sy: float, width: int, height: int) -> tuple[float, float]:
        '''
            Converts screen pixels to world mm coordinates.

            :param sx: Screen X pixel coordinate.
            :param sy: Screen Y pixel coordinate.
            :param width: Canvas pixel width.
            :param height: Canvas pixel height.
            :return: Tuple of world (wx, wy) coordinates in mm.
            :exceptions: None.
        '''
        cx: float = width / 2.0 + self.pan_x
        cy: float = height / 2.0 + self.pan_y
        return ((sx - cx) / self.scale, (cy - sy) / self.scale)

    def zoom_in(self) -> None:
        '''
            Increases zoom scale by factor.

            :exceptions: None.
        '''
        self.scale = min(self.ZOOM_MAX, self.scale * self.ZOOM_IN_FACTOR)

    def zoom_out(self) -> None:
        '''
            Decreases zoom scale by factor.

            :exceptions: None.
        '''
        self.scale = max(self.ZOOM_MIN, self.scale * self.ZOOM_OUT_FACTOR)

    def reset(self) -> None:
        '''
            Resets scale and pan offset to defaults.

            :exceptions: None.
        '''
        self.scale = self.DEFAULT_ZOOM
        self.pan_x = 0.0
        self.pan_y = 0.0

    def fit_reach(self, width: int, height: int) -> None:
        '''
            Adjusts scale and pan to fit robot reach boundary into window.

            :param width: Canvas width in pixels.
            :param height: Canvas height in pixels.
            :exceptions: None.
        '''
        if width > self.MIN_CANVAS_DIMENSION and height > self.MIN_CANVAS_DIMENSION:
            min_dim: float = float(min(width, height))
            self.scale = (min_dim * self.REACH_COVERAGE_RATIO) / self.R_MAX_MM
            self.pan_x = 0.0
            self.pan_y = 0.0
