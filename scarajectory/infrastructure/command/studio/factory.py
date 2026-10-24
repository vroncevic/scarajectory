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
    Factory responsible for instantiating and wiring studio command components.
'''

from __future__ import annotations

from scarajectory.infrastructure.command.bundle import CommandBundle
from scarajectory.infrastructure.command.idefinition import ICommandDefinition
from scarajectory.infrastructure.command.iexecutor import ICommandExecutor
from scarajectory.infrastructure.command.studio.definition import StudioCommandDefinition
from scarajectory.infrastructure.command.studio.dependencies import StudioDependencies
from scarajectory.infrastructure.command.studio.executor import StudioCommandExecutor
from scarajectory.infrastructure.command.studio.provides import StudioProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class StudioFactory:
    '''
        Factory creating studio command definition, executor, and bundle.

        It defines:

            :methods:
                | create - Creates StudioProvides container with wired command bundle.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: StudioDependencies) -> StudioProvides:
        '''
            Creates StudioProvides container with wired command bundle.

            :param dependencies: Injected StudioDependencies holding GUI adapter.
            :return: StudioProvides container.
            :exceptions: None.
        '''
        definition: ICommandDefinition = StudioCommandDefinition()
        executor: ICommandExecutor[ICommandDefinition, object, object, object] = (
            StudioCommandExecutor(definition=definition, gui=dependencies.gui)
        )
        command_bundle = CommandBundle(definition=definition, executor=executor)

        return StudioProvides(
            command_bundle=command_bundle,
            definition=definition,
            executor=executor,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Factory version string.
            :exceptions: None.
        '''
        return __version__
