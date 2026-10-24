# -*- coding: UTF-8 -*-

'''
Module
    ieditor.py
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
    Defines interface IWaypointEditor for trajectory waypoint editor widgets.
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
class IWaypointEditor(Protocol):
    '''
        Contract for waypoint editor widgets combining tabular display and coordinate inputs.

        It defines:

            :methods:
                | delete_selected - Deletes currently selected waypoint.
                | refresh_table - Refreshes table rows from active plan.
                | apply_point_edit - Applies coordinate edits to selected waypoint.
                | on_trajectory_updated - Populates coordinate entries on plan changes.
                | get_version - Returns component version string.
    '''

    def delete_selected(self) -> None:
        '''
            Deletes currently selected waypoint.
        '''

    def refresh_table(self) -> None:
        '''
            Refreshes table rows from active plan.
        '''

    def apply_point_edit(self) -> None:
        '''
            Applies coordinate edits to selected waypoint.
        '''

    def on_trajectory_updated(self) -> None:
        '''
            Populates coordinate entries on plan changes.
        '''

    def get_version(self) -> str:
        '''
            Returns component version string.

            :return: Component version string.
        '''
