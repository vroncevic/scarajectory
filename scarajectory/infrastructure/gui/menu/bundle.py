# -*- coding: UTF-8 -*-

'''
Module
    bundle.py
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
    Container bundle holding menu bar collaborator dependencies.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.itrajectory_history import ITrajectoryHistory
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore
from scarajectory.infrastructure.gui.canvas.navigation.icanvas_view_navigator import ICanvasViewNavigator
from scarajectory.infrastructure.gui.editor.table.itable import ITable

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True)
class MenuBundle:
    '''
        Immutable data container holding application menu bar collaborators.

        It defines:

            :attributes:
                | store - Waypoint store interface.
                | mutation - Plan bulk mutation interface.
                | history - Trajectory history interface.
                | storage - Plan storage service interface.
                | dsl_service - SCARA DSL service interface.
                | navigator - Viewport navigation interface.
                | table - Waypoint table interface.
    '''

    store: IWaypointStore
    mutation: IPlanBulkMutator
    history: ITrajectoryHistory
    storage: IPlanStorageService
    dsl_service: IScaraDslService
    navigator: ICanvasViewNavigator
    table: ITable
