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
    Factory instantiating and assembling hardware sub-controllers for tabs.
'''

from __future__ import annotations

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.infrastructure.protocol.builder.factory import BuilderFactory

from scarajectory.infrastructure.gui.controls.controllers.bundle import TabControllersBundle
from scarajectory.infrastructure.manipulator.dependencies import ManipulatorDependencies
from scarajectory.infrastructure.manipulator.factory import ManipulatorFactory
from scarajectory.infrastructure.manipulator.provides import ManipulatorProvides
from scarajectory.infrastructure.tool.dependencies import ToolDependencies
from scarajectory.infrastructure.tool.factory import ToolFactory
from scarajectory.infrastructure.tool.provides import ToolProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TabControllersFactory:
    '''
        Factory instantiating and assembling hardware sub-controllers for tabs.

        It defines:

            :methods:
                | create - Constructs hardware sub-controllers for tabs.
                | get_version - Returns factory version string.
    '''

    @classmethod
    def create(
        cls,
        raw_channel: IRawChannel,
    ) -> TabControllersBundle:
        '''
            Constructs and bundles hardware sub-controllers.

            :param raw_channel: Active communication channel.
            :return: Assembled TabControllersBundle instance.
        '''
        builders = BuilderFactory.create()
        manipulator_provides: ManipulatorProvides = ManipulatorFactory.create(
            ManipulatorDependencies(
                raw_channel=raw_channel,
                system_builder=builders.system,
                frame_packer=builders.packer,
            )
        )
        tool_provides: ToolProvides = ToolFactory.create(
            ToolDependencies(
                raw_channel=raw_channel,
                actuator_builder=builders.actuator,
                frame_packer=builders.packer,
            )
        )

        return TabControllersBundle(
            motion_ctrl=manipulator_provides.motion_controller,
            jog_ctrl=manipulator_provides.jog_controller,
            tool_ctrl=tool_provides.tool_controller,
            query_ctrl=manipulator_provides.query_controller,
        )

    @classmethod
    def get_version(cls) -> str:
        '''
            Returns component version string.

            :return: Version string.
        '''
        return __version__
