# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory instantiating CanvasShapeHandler components.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.canvas.handler.coordinator.icoordinator import IShapePlanCoordinator
from scarajectory.infrastructure.gui.canvas.handler.shape.handler import CanvasShapeHandler

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasShapeHandlerFactory:
    '''
        Factory providing creation methods for CanvasShapeHandler instances.

        It defines:

            :methods:
                | create - Constructs shape handler from injected coordinator.
                | get_version - Returns factory component version string.
    '''

    @classmethod
    def create(
        cls,
        *,
        coordinator: IShapePlanCoordinator,
    ) -> CanvasShapeHandler:
        '''
            Constructs shape handler instance from injected coordinator.

            :param coordinator: Injected IShapePlanCoordinator instance.
            :return: Configured CanvasShapeHandler instance.
            :exceptions: None.
        '''
        return CanvasShapeHandler(coordinator=coordinator)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory component version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
