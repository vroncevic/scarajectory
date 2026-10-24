# -*- coding: UTF-8 -*-

'''
Module
    factory.py
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
    Factory service constructing ToolProvides subsystem containers.
'''

from __future__ import annotations

from scarajectory.infrastructure.connection.dispatcher.dependencies import DispatcherDependencies
from scarajectory.infrastructure.connection.dispatcher.factory import DispatcherFactory
from scarajectory.infrastructure.connection.dispatcher.provides import DispatcherProvides
from scarajectory.infrastructure.tool.controller.dependencies import ControllerDependencies
from scarajectory.infrastructure.tool.controller.factory import ControllerFactory
from scarajectory.infrastructure.tool.controller.provides import ControllerProvides
from scarajectory.infrastructure.tool.dependencies import ToolDependencies
from scarajectory.infrastructure.tool.provides import ToolProvides
from scarajectory.infrastructure.tool.worker.factory import WorkerFactory
from scarajectory.infrastructure.tool.worker.provides import WorkerProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ToolFactory:
    '''
        Subsystem factory providing creation and assembly of ToolProvides interfaces.

        It defines:

            :methods:
                | create - Constructs ToolProvides subsystem container.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ToolDependencies) -> ToolProvides:
        '''
            Constructs and wires the tool subsystem into a ToolProvides container.

            :param dependencies: Injected ToolDependencies parameter bundle.
            :return: ToolProvides instance exposing toolhead services.
            :exceptions: None.
        '''
        worker_provides: WorkerProvides = WorkerFactory.create()
        dispatcher_provides: DispatcherProvides = DispatcherFactory.create(
            DispatcherDependencies(
                raw_channel=dependencies.raw_channel,
                frame_packer=dependencies.frame_packer,
            )
        )
        controller_provides: ControllerProvides = ControllerFactory.create(
            ControllerDependencies(
                channel_dispatcher=dispatcher_provides.channel_dispatcher,
                actuator_builder=dependencies.actuator_builder,
                pulse_runner=worker_provides.pulse_runner,
            )
        )

        return ToolProvides(tool_controller=controller_provides.tool_controller)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
