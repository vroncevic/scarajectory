# -*- coding: UTF-8 -*-

'''
Module
    factory_test.py
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
    Unit tests for TabControllersFactory instantiation service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaracom.bridge.transceiver.ichannel import IRawChannel

from scaralang.core.service.protocol.iactuator_builder import IBinaryActuatorFrameBuilder
from scaralang.core.service.protocol.ipacker import IBinaryFramePacker
from scaralang.core.service.protocol.isystem_builder import IBinarySystemFrameBuilder

from scarajectory.core.service.manipulator.ijog import IJogController
from scarajectory.core.service.manipulator.imotion import IMotionController
from scarajectory.core.service.manipulator.iquery import IQueryController
from scarajectory.core.service.tool.icontroller import IToolController
from scarajectory.infrastructure.gui.controls.controllers.bundle import TabControllersBundle
from scarajectory.infrastructure.gui.controls.controllers.factory import TabControllersFactory
from scarajectory.infrastructure.manipulator.dependencies import ManipulatorDependencies
from scarajectory.infrastructure.manipulator.provides import ManipulatorProvides
from scarajectory.infrastructure.tool.dependencies import ToolDependencies
from scarajectory.infrastructure.tool.provides import ToolProvides

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.3'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class TabControllersFactoryTestCase(TestCase):
    '''
        Tests TabControllersFactory component creation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create - Verifies assembly of sub-controllers.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''
            Verifies factory version string and create callable.

            :exceptions: None.
        '''
        self.assertEqual(TabControllersFactory.get_version(), '1.0.3')
        self.assertTrue(hasattr(TabControllersFactory, 'create'))
        self.assertTrue(callable(TabControllersFactory.create))

    def test_factory_create(self) -> None:
        '''
            Verifies assembling sub-controllers.

            :exceptions: None.
        '''
        target_pkg = (
            'scarajectory.infrastructure.gui.controls.controllers.factory.'
        )
        with (
            patch(f'{target_pkg}BuilderFactory.create') as mock_bld,
            patch(f'{target_pkg}ManipulatorFactory.create') as mock_manip,
            patch(f'{target_pkg}ToolFactory.create') as mock_tool,
        ):
            mock_system = MagicMock(spec=IBinarySystemFrameBuilder)
            mock_packer = MagicMock(spec=IBinaryFramePacker)
            mock_actuator = MagicMock(spec=IBinaryActuatorFrameBuilder)
            mock_bld.return_value.system = mock_system
            mock_bld.return_value.packer = mock_packer
            mock_bld.return_value.actuator = mock_actuator
            mock_motion = MagicMock(spec=IMotionController)
            mock_jog = MagicMock(spec=IJogController)
            mock_query = MagicMock(spec=IQueryController)
            mock_manip.return_value = ManipulatorProvides(
                jog_controller=mock_jog,
                motion_controller=mock_motion,
                query_controller=mock_query,
            )
            mock_tool_inst = MagicMock(spec=IToolController)
            mock_tool.return_value = ToolProvides(
                tool_controller=mock_tool_inst
            )

            raw_channel = MagicMock(spec=IRawChannel)
            bundle = TabControllersFactory.create(raw_channel)

            self.assertIsInstance(bundle, TabControllersBundle)
            self.assertIs(bundle.motion_ctrl, mock_motion)
            self.assertIs(bundle.jog_ctrl, mock_jog)
            self.assertIs(bundle.tool_ctrl, mock_tool_inst)
            self.assertIs(bundle.query_ctrl, mock_query)
            mock_manip.assert_called_once_with(
                ManipulatorDependencies(
                    raw_channel=raw_channel,
                    system_builder=mock_system,
                    frame_packer=mock_packer,
                )
            )
            mock_tool.assert_called_once_with(
                ToolDependencies(
                    raw_channel=raw_channel,
                    actuator_builder=mock_actuator,
                    frame_packer=mock_packer,
                )
            )


if __name__ == '__main__':
    main()
