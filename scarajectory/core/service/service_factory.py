# -*- coding: UTF-8 -*-

'''
Module
    service_factory.py
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
    Factory module for assembling and instantiating Service instances.
'''

from __future__ import annotations

from scarajectory.core.service.trajectory.plan.itrajectory_plan import ITrajectoryPlan
from scarajectory.core.service.trajectory.contract.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.communication.stream.itrajectory_streamer import ITrajectoryStreamer
from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scarajectory.core.service.engine import Service

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ServiceFactory:
    '''
        Factory responsible for assembling and instantiating Service instances.

        It defines:

            :methods:
                | create - Assembles and instantiates a Service instance.
    '''

    @classmethod
    def create(
        cls,
        validator: ITrajectoryValidator,
        streamer: ITrajectoryStreamer,
        storage: IPlanStorageService,
        plan: ITrajectoryPlan,
        dsl_service: IScaraDslService,
    ) -> Service:
        '''
            Assembles and instantiates a Service facade instance.

            :param validator: ITrajectoryValidator instance.
            :param streamer: ITrajectoryStreamer instance.
            :param storage: IPlanStorageService instance.
            :param plan: ITrajectoryPlan instance.
            :param dsl_service: IScaraDslService instance.
            :return: Fully assembled Service instance.
            :exceptions: None.
        '''
        return Service(
            validator=validator,
            streamer=streamer,
            storage=storage,
            plan=plan,
            dsl_service=dsl_service,
        )
