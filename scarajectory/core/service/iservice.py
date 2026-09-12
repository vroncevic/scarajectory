# -*- coding: UTF-8 -*-

'''
Module
    iservice.py
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
    Defines interface IService for trajectory business logic and subsystem orchestration.
'''

from __future__ import annotations

from typing import Protocol, runtime_checkable

from scarajectory.core.model.trajectory.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.communication.itrajectory_streamer import ITrajectoryStreamer
from scarajectory.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.trajectory.iplan_command_service import IPlanCommandService
from scarajectory.core.service.trajectory.iplan_persistence_service import IPlanPersistenceService
from scarajectory.core.service.trajectory.iplan_validation_service import IPlanValidationService

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@runtime_checkable
class IService(
    IPlanCommandService,
    IPlanPersistenceService,
    IPlanValidationService,
    Protocol
):
    '''
        Composite interface for orchestrating trajectory operations and services.

        It defines:

            :methods:
                | is_initialized - Checks if the service is properly initialized.
                | get_plan - Returns the active ITrajectoryPlan.
                | get_storage - Returns the active IPlanStorageService.
                | get_validator - Returns the active ITrajectoryValidator.
                | get_streamer - Returns the active ITrajectoryStreamer.
                | get_dsl_service - Returns the active IScaraDslService.
    '''

    def is_initialized(self) -> bool:
        '''
            Checks if the service is properly initialized.

            :return: True if initialized, False otherwise.
        '''

    def get_plan(self) -> ITrajectoryPlan:
        '''
            Returns the active ITrajectoryPlan.

            :return: ITrajectoryPlan instance.
        '''

    def get_storage(self) -> IPlanStorageService:
        '''
            Returns the active IPlanStorageService.

            :return: IPlanStorageService instance.
        '''

    def get_validator(self) -> ITrajectoryValidator:
        '''
            Returns the active ITrajectoryValidator.

            :return: ITrajectoryValidator instance.
        '''

    def get_streamer(self) -> ITrajectoryStreamer:
        '''
            Returns the active ITrajectoryStreamer.

            :return: ITrajectoryStreamer instance.
        '''

    def get_dsl_service(self) -> IScaraDslService:
        '''
            Returns the active IScaraDslService.

            :return: IScaraDslService instance.
        '''

