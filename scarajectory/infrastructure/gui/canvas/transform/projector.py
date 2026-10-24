# -*- coding: UTF-8 -*-

'''
Module
    projector.py
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
    Coordinates mapping between world millimeters and screen pixels.
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


class CoordinateProjector:
    '''
        Manages coordinate mapping between world millimeters and canvas screen pixels.

        It defines:

            :attributes:
                | CENTER_DIVISOR - Divisor constant for calculating midpoint origin.
                | _transform - Injected ViewportTransform state carrier.
            :methods:
                | __init__ - Initializes projector with viewport transform state.
                | world_to_screen - Converts world mm coordinates to canvas screen pixels.
                | screen_to_world - Converts screen pixels to world mm coordinates.
    '''

    CENTER_DIVISOR: ClassVar[float] = 2.0

    _transform: ViewportTransform

    def __init__(self, transform: ViewportTransform) -> None:
        '''
            Initializes projector with viewport transform state.

            :param transform: ViewportTransform state carrier.
            :exceptions: None.
        '''
        self._transform: Final[ViewportTransform] = transform

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
        cx: float = width / self.CENTER_DIVISOR + self._transform.pan_x
        cy: float = height / self.CENTER_DIVISOR + self._transform.pan_y

        return (cx + x * self._transform.scale, cy - y * self._transform.scale)

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
        cx: float = width / self.CENTER_DIVISOR + self._transform.pan_x
        cy: float = height / self.CENTER_DIVISOR + self._transform.pan_y

        return (
            (sx - cx) / self._transform.scale,
            (cy - sy) / self._transform.scale,
        )
