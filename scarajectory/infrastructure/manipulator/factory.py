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
    Canonical factory service constructing ManipulatorProvides subsystem components.
'''

from __future__ import annotations

from scarajectory.infrastructure.manipulator.dependencies import ManipulatorDependencies
from scarajectory.infrastructure.manipulator.jog.dependencies import JogDependencies
from scarajectory.infrastructure.manipulator.jog.factory import JogControllerFactory
from scarajectory.infrastructure.manipulator.jog.provides import JogProvides
from scarajectory.infrastructure.manipulator.motion.dependencies import MotionDependencies
from scarajectory.infrastructure.manipulator.motion.factory import MotionControllerFactory
from scarajectory.infrastructure.manipulator.motion.provides import MotionProvides
from scarajectory.infrastructure.manipulator.provides import ManipulatorProvides
from scarajectory.infrastructure.manipulator.query.dependencies import QueryDependencies
from scarajectory.infrastructure.manipulator.query.factory import QueryControllerFactory
from scarajectory.infrastructure.manipulator.query.provides import QueryProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorFactory:
    '''
        Factory providing creation of ManipulatorProvides subsystem components.

        It defines:

            :methods:
                | create - Constructs and returns a ManipulatorProvides instance.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(cls, dependencies: ManipulatorDependencies) -> ManipulatorProvides:
        '''
            Constructs and returns a ManipulatorProvides instance with wired sub-factories.

            :param dependencies: Injected ManipulatorDependencies bundle.
            :return: Configured ManipulatorProvides instance.
        '''
        jog_provides: JogProvides = JogControllerFactory.create(
            JogDependencies(
                raw_channel=dependencies.raw_channel,
                system_builder=dependencies.system_builder,
                frame_packer=dependencies.frame_packer,
            )
        )
        motion_provides: MotionProvides = MotionControllerFactory.create(
            MotionDependencies(
                raw_channel=dependencies.raw_channel,
                system_builder=dependencies.system_builder,
                frame_packer=dependencies.frame_packer,
            )
        )
        query_provides: QueryProvides = QueryControllerFactory.create(
            QueryDependencies(
                raw_channel=dependencies.raw_channel,
                system_builder=dependencies.system_builder,
                frame_packer=dependencies.frame_packer,
            )
        )

        return ManipulatorProvides(
            jog_controller=jog_provides.jog_controller,
            motion_controller=motion_provides.motion_controller,
            query_controller=query_provides.query_controller,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns factory version string.

            :return: Version string in SemVer format.
        '''
        return __version__
