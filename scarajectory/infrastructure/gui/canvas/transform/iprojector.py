# -*- coding: UTF-8 -*-

'''
Module
    iprojector.py
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
    Defines structural protocol ICoordinateProjector for 2D viewport coordinate projections.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ICoordinateProjector(Protocol):
    '''
        Structural protocol defining coordinate mapping between millimeters and screen pixels.

        It defines:

            :methods:
                | world_to_screen - Converts world mm coordinates to canvas screen pixels.
                | screen_to_world - Converts screen pixels to world mm coordinates.
    '''

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
        '''

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
        '''
