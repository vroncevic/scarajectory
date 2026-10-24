# -*- coding: UTF-8 -*-

'''
Module
    transform.py
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
                | CENTER_DIVISOR - Divisor constant for calculating midpoint origin.
                | scale - Active zoom scale.
                | pan_x - Horizontal pan offset in pixels.
                | pan_y - Vertical pan offset in pixels.
            :methods:
                | __init__ - Initializes default zoom scale and zero pan offset.
                | world_to_screen - Converts world mm coordinates to canvas screen pixels.
                | screen_to_world - Converts screen pixels to world mm coordinates.
    '''

    DEFAULT_ZOOM: ClassVar[float] = 1.35
    CENTER_DIVISOR: ClassVar[float] = 2.0

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

    def world_to_screen(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
    ) -> tuple[float, float]:
        '''
            Converts world mm coordinates to canvas screen pixels.

            :param x: World X coordinate in mm.
            :param y: World Y coordinate in mm.
            :param width: Canvas pixel width.
            :param height: Canvas pixel height.
            :return: Tuple of screen (sx, sy) pixel coordinates.
            :exceptions: None.
        '''
        cx: float = width / self.CENTER_DIVISOR + self.pan_x
        cy: float = height / self.CENTER_DIVISOR + self.pan_y

        return (cx + x * self.scale, cy - y * self.scale)

    def screen_to_world(
        self,
        sx: float,
        sy: float,
        width: int,
        height: int,
    ) -> tuple[float, float]:
        '''
            Converts screen pixels to world mm coordinates.

            :param sx: Screen X pixel coordinate.
            :param sy: Screen Y pixel coordinate.
            :param width: Canvas pixel width.
            :param height: Canvas pixel height.
            :return: Tuple of world (wx, wy) coordinates in mm.
            :exceptions: None.
        '''
        cx: float = width / self.CENTER_DIVISOR + self.pan_x
        cy: float = height / self.CENTER_DIVISOR + self.pan_y

        return ((sx - cx) / self.scale, (cy - sy) / self.scale)
