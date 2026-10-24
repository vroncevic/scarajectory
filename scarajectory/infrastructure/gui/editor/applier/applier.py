# -*- coding: UTF-8 -*-

'''
Module
    applier.py
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
from typing import ClassVar

from scarajectory.core.model.trajectory.waypoint import TrajectoryWaypoint
from scarajectory.infrastructure.gui.editor.applier.inputs import WaypointCoordinateInputs
from scarajectory.infrastructure.gui.editor.table.bundle import TableBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class WaypointEditApplier:
    '''
        Validates coordinate strings and applies updates to the selected waypoint.

        It defines:

            :constants:
                | TITLE_ERROR - Message box title on input conversion failure.
                | MSG_ERROR - Error message reported on invalid numeric values.
                | TITLE_VALIDATION - Message box title on kinematic validation failure.
                | MSG_OUT_OF_BOUNDS - Error message reported on out-of-reach coordinates.
            :methods:
                | apply_edit - Validates coordinates and updates waypoint in mutation service.
                | get_version - Returns applier version string.
    '''

    TITLE_ERROR: ClassVar[str] = 'Input Error'
    MSG_ERROR: ClassVar[str] = 'Invalid numeric values.'
    TITLE_VALIDATION: ClassVar[str] = 'Kinematic Error'
    MSG_OUT_OF_BOUNDS: ClassVar[str] = (
        'Waypoint coordinates violate SCARA reachability or kinematic bounds.'
    )

    def apply_edit(
        self,
        *,
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
                cur: TrajectoryWaypoint = bundle.store.waypoints[idx]
                updated = TrajectoryWaypoint(
                    x=float(inputs.x),
                    y=float(inputs.y),
                    z=float(inputs.z),
                    phi=float(inputs.phi),
                    speed=float(inputs.speed),
                    name=cur.name,
                    command=cur.command,
                )

                if not bundle.validator.validate_point(updated).is_valid:
                    showerror(self.TITLE_VALIDATION, self.MSG_OUT_OF_BOUNDS)
                    return False

                bundle.mutation.update_point(idx, updated)
                return True

            except ValueError:
                showerror(self.TITLE_ERROR, self.MSG_ERROR)
                return False

        return False

    def get_version(self) -> str:
        '''
            Returns applier version string.

            :return: Version string.
            :exceptions: None.
        '''
        return __version__
