# -*- coding: UTF-8 -*-

'''
Module
    manipulator_controllers_factory_test.py
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
    Unit tests for ManipulatorControllersFactory instantiation service.
'''

from __future__ import annotations

from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from scaralang.core.service.protocol.ibinary_frame_builder import (
    IBinaryFrameBuilder,
)
from scarajectory.core.model.protocol.protocol_mode import ProtocolMode
from scarajectory.core.service.connection.iraw_channel import IRawChannel
from scarajectory.infrastructure.gui.controls.manipulator_controllers_bundle import (
    ManipulatorControllersBundle,
)
from scarajectory.infrastructure.gui.controls.manipulator_controllers_factory import (
    ManipulatorControllersFactory,
)
from scarajectory.infrastructure.manipulator.jog_controller import JogController
from scarajectory.infrastructure.manipulator.motion_controller import (
    MotionController,
)
from scarajectory.infrastructure.manipulator.query_controller import (
    QueryController,
)
from scarajectory.infrastructure.tool.tool_controller import ToolController

__author__ = 'Vladimir Roncevic'
__copyright__ = '(C) 2026, https://vroncevic.github.io/scarajectory'
__credits__ = ['Vladimir Roncevic', 'Python Software Foundation']
__license__ = 'https://github.com/vroncevic/scarajectory/blob/dev/LICENSE'
__version__ = '1.0.4'
__maintainer__ = 'Vladimir Roncevic'
__email__ = 'elektron.ronca@gmail.com'
__status__ = 'Updated'


class ManipulatorControllersFactoryTestCase(TestCase):
    '''
        Tests ManipulatorControllersFactory component creation.

        It defines:

            :methods:
                | test_factory_version_and_structure - Verifies version and structure.
                | test_factory_create_default_binary - Verifies assembly with default binary mode.
                | test_factory_create_ascii_mode - Verifies assembly with explicit ASCII mode.
    '''

    def test_factory_version_and_structure(self) -> None:
        '''Verifies factory version string and create callable.'''
        self.assertEqual(ManipulatorControllersFactory.get_version(), '1.0.4')
        self.assertTrue(hasattr(ManipulatorControllersFactory, 'create'))
        self.assertTrue(callable(ManipulatorControllersFactory.create))

    def test_factory_create_default_binary(self) -> None:
        '''Verifies assembling sub-controllers with default binary protocol mode.'''
        target_pkg = (
            'scarajectory.infrastructure.gui.controls.'
            'manipulator_controllers_factory.'
        )
        with (
            patch(f'{target_pkg}BinaryFrameBuilderFactory.create') as mock_bld,
            patch(f'{target_pkg}MotionControllerFactory.create') as mock_mot,
            patch(f'{target_pkg}JogControllerFactory.create') as mock_jog,
            patch(f'{target_pkg}ToolControllerFactory.create') as mock_tool,
            patch(f'{target_pkg}QueryControllerFactory.create') as mock_qry,
        ):
            mock_builder = MagicMock(spec=IBinaryFrameBuilder)
            mock_bld.return_value = mock_builder
            mock_motion = MagicMock(spec=MotionController)
            mock_mot.return_value = mock_motion
            mock_jog_inst = MagicMock(spec=JogController)
            mock_jog.return_value = mock_jog_inst
            mock_tool_inst = MagicMock(spec=ToolController)
            mock_tool.return_value = mock_tool_inst
            mock_query = MagicMock(spec=QueryController)
            mock_qry.return_value = mock_query

            raw_channel = MagicMock(spec=IRawChannel)
            bundle = ManipulatorControllersFactory.create(raw_channel)

            self.assertIsInstance(bundle, ManipulatorControllersBundle)
            self.assertIs(bundle.motion_ctrl, mock_motion)
            self.assertIs(bundle.jog_ctrl, mock_jog_inst)
            self.assertIs(bundle.tool_ctrl, mock_tool_inst)
            self.assertIs(bundle.query_ctrl, mock_query)
            mock_mot.assert_called_once_with(
                raw_channel=raw_channel,
                frame_builder=mock_builder,
                protocol_mode=ProtocolMode.BINARY,
            )

    def test_factory_create_ascii_mode(self) -> None:
        '''Verifies assembling sub-controllers with explicit ASCII protocol mode.'''
        target_pkg = (
            'scarajectory.infrastructure.gui.controls.'
            'manipulator_controllers_factory.'
        )
        with (
            patch(f'{target_pkg}BinaryFrameBuilderFactory.create') as mock_bld,
            patch(f'{target_pkg}MotionControllerFactory.create') as mock_mot,
            patch(f'{target_pkg}JogControllerFactory.create') as mock_jog,
            patch(f'{target_pkg}ToolControllerFactory.create') as mock_tool,
            patch(f'{target_pkg}QueryControllerFactory.create') as mock_qry,
        ):
            raw_channel = MagicMock(spec=IRawChannel)
            bundle = ManipulatorControllersFactory.create(
                raw_channel,
                protocol_mode=ProtocolMode.ASCII,
            )

            self.assertIsInstance(bundle, ManipulatorControllersBundle)
            mock_bld.assert_called_once()
            mock_mot.assert_called_once()
            mock_jog.assert_called_once()
            mock_tool.assert_called_once()
            mock_qry.assert_called_once()


if __name__ == '__main__':
    main()
