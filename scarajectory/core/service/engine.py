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
    Core service implementation orchestrating trajectory modeling, validation, storage, dsl, and streaming.
'''

from __future__ import annotations

from typing import Final

from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.communication.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.dsl.scara_dsl_service import ScaraDslService

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
        Service orchestrating trajectory domain modeling, validation, storage, and execution.

        It defines:

            :attributes:
                | _plan - Trajectory plan domain abstraction.
                | _storage - Dedicated plan serialization and storage service.
                | _validator - Kinematic reachability validator.
                | _streamer - Robot communication and motion streamer.
                | _dsl_service - High-level SCARA DSL compilation and export service.
            :methods:
                | __init__ - Initializes the service with injected abstractions.
                | is_initialized - Checks if the service is properly initialized.
                | get_plan - Returns the active ITrajectoryPlan.
                | get_storage - Returns the active IPlanStorageService.
                | get_validator - Returns the active ITrajectoryValidator.
                | get_streamer - Returns the active ITrajectoryStreamer.
                | get_dsl_service - Returns the active IScaraDslService.
                | validate_plan - Validates the current trajectory plan.
                | save_plan - Saves current plan to file path.
                | load_plan - Loads plan from file path.
                | clear_plan - Clears all waypoints from active plan.
                | undo - Reverts last plan modification.
                | redo - Re-applies undone plan modification.
                | new_plan - Resets active plan to empty state.
    '''

    _plan: ITrajectoryPlan
    _storage: IPlanStorageService
    _validator: ITrajectoryValidator
    _streamer: ITrajectoryStreamer
    _dsl_service: IScaraDslService

    def __init__(
        self,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        storage: IPlanStorageService,
        plan: ITrajectoryPlan,
        dsl_service: IScaraDslService | None = None
    ) -> None:
        '''
            Initializes the service with injected abstractions.

            :param validator: ITrajectoryValidator instance.
            :param streamer: ITrajectoryStreamer instance.
            :param storage: IPlanStorageService instance.
            :param plan: ITrajectoryPlan instance.
            :param dsl_service: Optional IScaraDslService instance.
        '''
        self._validator: Final[ITrajectoryValidator] = validator
        self._streamer: Final[ITrajectoryStreamer] = streamer
        self._storage: Final[IPlanStorageService] = storage
        self._plan: Final[ITrajectoryPlan] = plan
        self._dsl_service: Final[IScaraDslService] = (
            dsl_service or ScaraDslService(validator=validator)
        )

    def is_initialized(self) -> bool:
        '''
            Checks if the service is properly initialized.

            :return: True if initialized, False otherwise.
        '''
        return (
            self._plan is not None and
            self._validator is not None and
            self._streamer is not None and
            self._storage is not None and
            self._dsl_service is not None
        )

    def get_plan(self) -> ITrajectoryPlan:
        '''
            Returns the active ITrajectoryPlan.

            :return: ITrajectoryPlan instance.
        '''
        return self._plan

    def get_storage(self) -> IPlanStorageService:
        '''
            Returns the active IPlanStorageService.

            :return: IPlanStorageService instance.
        '''
        return self._storage

    def get_validator(self) -> ITrajectoryValidator:
        '''
            Returns the active ITrajectoryValidator.

            :return: ITrajectoryValidator instance.
        '''
        return self._validator

    def get_streamer(self) -> ITrajectoryStreamer:
        '''
            Returns the active ITrajectoryStreamer.

            :return: ITrajectoryStreamer instance.
        '''
        return self._streamer

    def get_dsl_service(self) -> IScaraDslService:
        '''
            Returns the active IScaraDslService.

            :return: IScaraDslService instance.
        '''
        return self._dsl_service

    def validate_plan(self) -> tuple[bool, list[str]]:
        '''
            Validates the current trajectory plan against robot kinematic bounds.

            :return: Tuple of (is_valid, messages_list).
        '''
        return self._validator.validate_plan(self._plan)

    def save_plan(self, filepath: str) -> None:
        '''
            Saves current plan to file path.

            :param filepath: Target file path.
        '''
        self._storage.save_plan(self._plan, filepath)

    def load_plan(self, filepath: str) -> None:
        '''
            Loads plan from file path.

            :param filepath: Source file path.
        '''
        loaded_pts = self._storage.load_plan(filepath)
        self._plan.set_waypoints(loaded_pts)

    def clear_plan(self) -> None:
        '''
            Clears all waypoints from active plan.
        '''
        self._plan.clear()

    def undo(self) -> bool:
        '''
            Reverts last plan modification.

            :return: True if undone, False otherwise.
        '''
        return self._plan.undo()

    def redo(self) -> bool:
        '''
            Re-applies undone plan modification.

            :return: True if redone, False otherwise.
        '''
        return self._plan.redo()

    def new_plan(self) -> None:
        '''
            Resets active plan to empty state.
        '''
        self._plan.clear()

