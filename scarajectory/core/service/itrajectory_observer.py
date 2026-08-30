# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_observer.py
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
    Defines ITrajectoryObserver for decoupling model updates from GUI views.
'''

from __future__ import annotations

from abc import ABC, abstractmethod

__author__: str = 'Vladimir Roncevic'
__copyright__: str = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__: list[str] = ['Vladimir Roncevic', 'Python Software Foundation']
__license__: str = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.0'
__maintainer__: str = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ITrajectoryObserver(ABC):
    '''
        Contract for UI widgets and viewers listening to trajectory changes.

        It defines:

            :methods:
                | on_trajectory_updated - Called whenever points are added, modified, or cleared.
                | on_point_selected - Called when a specific waypoint is selected in canvas or table.
    '''

    @abstractmethod
    def on_trajectory_updated(self) -> None:
        '''
            Called whenever points are added, modified, reordered, or cleared.

            :exceptions: None.
        '''

    @abstractmethod
    def on_point_selected(self, index: int) -> None:
        '''
            Called when a specific waypoint is selected in canvas or table.

            :param index: Selected point index (-1 for none).
            :exceptions: None.
        '''
