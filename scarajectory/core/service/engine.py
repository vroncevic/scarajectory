# -*- coding: UTF-8 -*-

'''
Module
    engine.py
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
    Core service implementation orchestrating trajectory plan validation, persistence, and lifecycle.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.plan.mutation.iplan_bulk_mutator import IPlanBulkMutator
from scarajectory.core.service.trajectory.plan.store.iwaypoint_store import IWaypointStore

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class Service:
    '''
        Service orchestrating trajectory domain plan validation, persistence, and lifecycle.

        It defines:

            :attributes:
                | _validator - Kinematic reachability validator.
                | _storage - Dedicated plan serialization and storage service.
                | _store - Trajectory waypoint store.
                | _mutation - Trajectory plan bulk mutator.
            :methods:
                | __init__ - Initializes the service with injected abstractions.
                | validator - Returns the active ITrajectoryValidator.
                | is_initialized - Checks if the service is properly initialized.
                | validate_plan - Validates the current trajectory plan.
                | save_plan - Saves current plan to file path.
                | load_plan - Loads plan from file path.
                | clear_plan - Clears all waypoints from active plan.
    '''

    _validator: ITrajectoryValidator
    _storage: IPlanStorageService
    _store: IWaypointStore
    _mutation: IPlanBulkMutator

    def __init__(
        self,
        validator: ITrajectoryValidator,
        storage: IPlanStorageService,
        store: IWaypointStore,
        mutation: IPlanBulkMutator,
    ) -> None:
        '''
            Initializes the service with injected abstractions.

            :param validator: ITrajectoryValidator instance.
            :param storage: IPlanStorageService instance.
            :param store: IWaypointStore instance.
            :param mutation: IPlanBulkMutator instance.
        '''
        self._validator: Final[ITrajectoryValidator] = validator
        self._storage: Final[IPlanStorageService] = storage
        self._store: Final[IWaypointStore] = store
        self._mutation: Final[IPlanBulkMutator] = mutation

    @property
    def validator(self) -> ITrajectoryValidator:
        '''
            Returns the active ITrajectoryValidator.

            :return: ITrajectoryValidator instance.
        '''
        return self._validator

    def is_initialized(self) -> bool:
        '''
            Checks if the service is properly initialized.

            :return: True if initialized, False otherwise.
        '''
        return True

    def validate_plan(self) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :return: Tuple of (is_valid, messages_list).
        '''
        return self._validator.validate_plan(self._store)

    def save_plan(self, filepath: str) -> None:
        '''
            Saves current plan to file path.

            :param filepath: Target file path.
        '''
        self._storage.save_plan(self._store, filepath)

    def load_plan(self, filepath: str) -> None:
        '''
            Loads plan from file path.

            :param filepath: Source file path.
        '''
        loaded_pts = self._storage.load_plan(filepath)
        self._mutation.set_waypoints(loaded_pts)

    def clear_plan(self) -> None:
        '''
            Clears all waypoints from active plan.
        '''
        self._mutation.clear()
