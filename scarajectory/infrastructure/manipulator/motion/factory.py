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
    Factory service constructing Motion controller subsystem components.
'''

from __future__ import annotations

from scarajectory.infrastructure.connection.dispatcher.dependencies import DispatcherDependencies
from scarajectory.infrastructure.connection.dispatcher.factory import DispatcherFactory
from scarajectory.infrastructure.connection.dispatcher.provides import DispatcherProvides
from scarajectory.infrastructure.manipulator.motion.controller import MotionController
from scarajectory.infrastructure.manipulator.motion.dependencies import MotionDependencies
from scarajectory.infrastructure.manipulator.motion.provides import MotionProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class MotionControllerFactory:
    '''
        Factory providing creation of Motion controller subsystem components.

        It defines:

            :methods:
                | create - Constructs Motion controller with injected dependencies.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: MotionDependencies) -> MotionProvides:
        '''
            Constructs and returns a MotionProvides container.

            :param dependencies: Injected MotionDependencies bundle.
            :return: Configured MotionProvides instance.
        '''
        dispatcher_provides: DispatcherProvides = DispatcherFactory.create(
            DispatcherDependencies(
                raw_channel=dependencies.raw_channel,
                frame_packer=dependencies.frame_packer,
            )
        )
        controller = MotionController(
            dispatcher=dispatcher_provides.channel_dispatcher,
            system_builder=dependencies.system_builder,
        )

        return MotionProvides(motion_controller=controller)

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string in SemVer format.
        '''
        return __version__
