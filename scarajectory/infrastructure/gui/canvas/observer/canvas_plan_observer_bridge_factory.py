# -*- coding: UTF-8 -*-

'''
Module
    canvas_plan_observer_bridge_factory.py
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
    Factory service for instantiating CanvasPlanObserverBridge objects.
'''

from __future__ import annotations

from collections.abc import Callable

from scarajectory.infrastructure.gui.canvas.observer.canvas_plan_observer_bridge import CanvasPlanObserverBridge

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasPlanObserverBridgeFactory:
    '''
        Factory providing instantiation of CanvasPlanObserverBridge components.

        It defines:

            :methods:
                | create - Constructs a CanvasPlanObserverBridge instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        redraw_action: Callable[[], None],
    ) -> CanvasPlanObserverBridge:
        '''
            Constructs a CanvasPlanObserverBridge instance.

            :param redraw_action: Callable triggering canvas redraw.
            :return: Configured CanvasPlanObserverBridge instance.
            :exceptions: None.
        '''
        return CanvasPlanObserverBridge(redraw_action)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Semantic version string.
            :exceptions: None.
        '''
        return __version__
