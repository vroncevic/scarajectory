# -*- coding: UTF-8 -*-

'''
Module
    waypoint_edit_applier.py
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
    Collaborator component parsing coordinate entries and applying waypoint modifications.
'''

from __future__ import annotations

from tkinter.messagebox import showerror

from scarajectory.core.model.trajectory.waypoint import Waypoint
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle
from scarajectory.infrastructure.gui.editor.waypoint_coordinate_inputs import WaypointCoordinateInputs

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditApplier:
    '''
        Validates coordinate strings and applies updates to the selected waypoint.

        It defines:

            :methods:
                | apply_edit - Validates coordinates and updates waypoint in mutation service.
                | get_version - Returns applier version string.
    '''

    @classmethod
    def apply_edit(
        cls,
        inputs: WaypointCoordinateInputs,
        bundle: TableBundle,
    ) -> bool:
        '''
            Validates coordinates and updates waypoint in mutation service.

            :param inputs: Injected WaypointCoordinateInputs container.
            :param bundle: Injected TableBundle dependency container.
            :return: True if edit was applied, False otherwise.
            :exceptions: None.
        '''
        idx: int = bundle.selection.selected_index

        if 0 <= idx < bundle.store.count:
            try:
                cur: Waypoint = bundle.store.waypoints[idx]
                updated = Waypoint(
                    x=float(inputs.x),
                    y=float(inputs.y),
                    z=float(inputs.z),
                    phi=float(inputs.phi),
                    speed=float(inputs.speed),
                    name=cur.name,
                    command=cur.command,
                )
                bundle.mutation.update_point(idx, updated)
                return True

            except ValueError:
                showerror('Input Error', 'Invalid numeric values.')
                return False

        return False

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns applier version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
