# -*- coding: UTF-8 -*-

'''
Module
    scarajectory_gui_init_bundle.py
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
    Parameter bundle holding external dependencies for ScarajectoryGUI assembly.
'''

from __future__ import annotations

from dataclasses import dataclass

from scaralang.core.service.dsl.iscara_dsl_service import IScaraDslService
from scaralang.core.service.trajectory.validation.itrajectory_validator import ITrajectoryValidator
from scarajectory.core.service.preferences.iconnection_repository import IConnectionRepository
from scarajectory.core.service.storage.iplan_storage_service import IPlanStorageService
from scarajectory.core.service.streaming.istream_playback_controller import IStreamPlaybackController
from scarajectory.infrastructure.streaming.bundle import StreamingBundle
from scarajectory.setup.pipeline.plan_pipeline_bundle import PlanPipelineBundle

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


@dataclass(slots=True, frozen=True, kw_only=True)
class ScarajectoryGUIInitBundle:
    '''
    Bundle containing external collaborators for GUI assembly.

    It defines:

        :attributes:
            | plan - Trajectory plan management pipeline bundle.
            | validator - Trajectory validation port.
            | streaming - Streaming subsystem services bundle.
            | storage - Trajectory plan disk storage service.
            | dsl_service - SCARA DSL interpretation service.
            | connection_repository - Connection preferences repository.
        :methods:
            | streamer - Returns playback controller for backward compatibility.
    '''

    plan: PlanPipelineBundle
    validator: ITrajectoryValidator
    streaming: StreamingBundle
    storage: IPlanStorageService
    dsl_service: IScaraDslService
    connection_repository: IConnectionRepository

    @property
    def streamer(self) -> IStreamPlaybackController:
        '''
        Returns motion streaming playback controller.

        :return: IStreamPlaybackController instance.
        '''
        return self.streaming.playback_controller
