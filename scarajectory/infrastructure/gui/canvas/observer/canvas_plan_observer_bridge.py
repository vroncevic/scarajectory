# -*- coding: UTF-8 -*-

'''
Module
    canvas_plan_observer_bridge.py
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
    Bridges domain plan notifications to canvas redraw requests.
'''

from __future__ import annotations

from collections.abc import Callable
from typing import Final

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class CanvasPlanObserverBridge:
    '''
        Bridges domain trajectory plan observer notifications to canvas redraw.

        It defines:

            :attributes:
                | _redraw_action - Callback invoked to redraw canvas scene.
            :methods:
                | __init__ - Initializes observer bridge with redraw callback.
                | on_trajectory_updated - Redraws canvas on plan modification.
                | on_point_selected - Redraws selection ring on point change.
    '''

    _redraw_action: Callable[[], None]

    def __init__(self, redraw_action: Callable[[], None]) -> None:
        '''
            Initializes the observer bridge with redraw callback.

            :param redraw_action: Callable triggering canvas redraw.
            :exceptions: None.
        '''
        self._redraw_action: Final[Callable[[], None]] = redraw_action

    def on_trajectory_updated(self) -> None:
        '''
            Redraws canvas on plan modification.

            :exceptions: None.
        '''
        self._redraw_action()

    def on_point_selected(self, index: int) -> None:
        '''
            Redraws selection ring when point selection changes.

            :param index: Selected waypoint index.
            :exceptions: None.
        '''
        _ = index
        self._redraw_action()
