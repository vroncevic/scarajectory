# -*- coding: UTF-8 -*-

'''
Module
    itrajectory_plan.py
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
    Composite structural interface protocol for complete trajectory plan domain model.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.itrajectory_mutable import ITrajectoryMutable
from scarajectory.core.model.trajectory.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.itrajectory_observer import ITrajectoryObserver

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class ITrajectoryPlan(ITrajectoryMutable, ITrajectoryHistory, Protocol):
    '''
        Composite structural interface protocol for a complete trajectory plan.

        It defines:

            :methods:
                | selected_index - Returns currently selected waypoint index.
                | set_selected_index - Selects waypoint at index.
                | add_observer - Registers plan mutation observer.
    '''

    @property
    def selected_index(self) -> int:
        '''
            Returns index of currently selected waypoint.

            :return: Selected waypoint index or -1.
        '''

    def set_selected_index(self, index: int) -> None:
        '''
            Selects a waypoint by index.

            :param index: Target index (-1 for deselect).
        '''

    def add_observer(self, observer: ITrajectoryObserver) -> None:
        '''
            Registers an observer widget.

            :param observer: ITrajectoryObserver instance.
        '''
