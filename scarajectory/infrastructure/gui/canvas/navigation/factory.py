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
    Factory constructing CanvasViewNavigator instances.
'''

from __future__ import annotations

from scarajectory.infrastructure.gui.canvas.navigation.dependencies import CanvasViewNavigatorDependencies
from scarajectory.infrastructure.gui.canvas.navigation.navigator import CanvasViewNavigator

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasViewNavigatorFactory:
    '''
        Factory constructing CanvasViewNavigator instances.

        It defines:

            :methods:
                | create - Constructs CanvasViewNavigator instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        dependencies: CanvasViewNavigatorDependencies,
    ) -> CanvasViewNavigator:
        '''
            Constructs and returns CanvasViewNavigator instance.

            :param dependencies: Injected CanvasViewNavigatorDependencies parameter bundle.
            :return: CanvasViewNavigator instance.
            :exceptions: None.
        '''
        return CanvasViewNavigator(
            dependencies.camera,
            dependencies.validator,
            dependencies.target,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
